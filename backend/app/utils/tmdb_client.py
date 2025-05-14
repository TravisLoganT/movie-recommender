import os
import requests
from typing import Dict, List, Any
from .error_handlers import (
    TMDBError,
    TMDBAPIError,
    TMDBInvalidIDError,
    TMDBInvalidQueryError,
    handle_api_response,
    validate_movie_id,
    validate_search_query,
    validate_page_number,
    validate_response_data
)

class TMDBClient:
    def __init__(self, api_key: str) -> None:
        self.base_url = 'https://api.themoviedb.org/3/'
        self.params = {
            'api_key': api_key
        }

    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make API request with error handling"""
        try:
            url = f"{self.base_url}{endpoint}"
            request_params = {**self.params, **(params or {})}
            
            response = requests.get(url, params=request_params)
            handle_api_response(response)
            
            return response.json()
        except requests.exceptions.RequestException as e:
            raise TMDBAPIError(f"Network error: {str(e)}")
        except TMDBAPIError:
            raise
        except Exception as e:
            raise TMDBError(f"Unexpected error: {str(e)}")

    def _format_movie(self, movie: Dict) -> Dict:
        """Format movie data"""
        poster_path = movie.get('poster_path')
        backdrop_path = movie.get('backdrop_path')
        
        return {
            'id': movie.get('id'),
            'title': movie.get('title'),
            'overview': movie.get('overview'),
            'poster_url': f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None,
            'backdrop_url': f"https://image.tmdb.org/t/p/original{backdrop_path}" if backdrop_path else None,
            'release_date': movie.get('release_date') or None,
            'rating': movie.get('vote_average'),
            'genres': movie.get('genre_ids', [])
        }

    def _format_movie_details(self, movie: Dict) -> Dict:
        """Format detailed movie data"""
        basic_info = self._format_movie(movie)
        return {
            **basic_info,
            'tagline': movie.get('tagline'),
            'runtime': movie.get('runtime'),
            'budget': movie.get('budget'),
            'revenue': movie.get('revenue'),
            'genres': [{'id': g['id'], 'name': g['name']} for g in movie.get('genres', [])],
            'production_companies': [{'id': c['id'], 'name': c['name']} for c in movie.get('production_companies', [])],
            'status': movie.get('status'),
            'original_language': movie.get('original_language')
        }

    def search_movies(self, query: str, page: int = 1, language: str = 'en-US') -> Dict:
        """Search for movies"""
        try:
            validate_search_query(query)
            validate_page_number(page)
            
            data = self._make_request('search/movie', {
                'query': query,
                'page': page,
                'language': language
            })
            
            validate_response_data(data, ['results', 'page'])
            
            return {
                'page': data.get('page'),
                'total_pages': data.get('total_pages'),
                'total_results': data.get('total_results'),
                'movies': [self._format_movie(movie) for movie in data.get('results', [])]
            }
        except (TMDBAPIError, TMDBInvalidQueryError) as e:
            raise
        except Exception as e:
            raise TMDBError(f"Error searching movies: {str(e)}")

    def get_movie_details(self, movie_id: int, language: str = 'en-US') -> Dict:
        """Get detailed information about a specific movie"""
        try:
            validate_movie_id(movie_id)
            
            data = self._make_request(f"movie/{movie_id}", {'language': language})
            validate_response_data(data, ['id', 'title'])
            
            return self._format_movie_details(data)
        except (TMDBAPIError, TMDBInvalidIDError) as e:
            raise
        except Exception as e:
            raise TMDBError(f"Error getting movie details: {str(e)}")

    def get_popular_movies(self, page: int = 1, language: str = 'en-US') -> Dict:
        """Get popular movies"""
        try:
            validate_page_number(page)
            
            data = self._make_request('movie/popular', {
                'page': page,
                'language': language
            })
            
            validate_response_data(data, ['results', 'page'])
            
            return {
                'page': data.get('page'),
                'total_pages': data.get('total_pages'),
                'total_results': data.get('total_results'),
                'movies': [self._format_movie(movie) for movie in data.get('results', [])]
            }
        except (TMDBAPIError, ValueError) as e:
            raise
        except Exception as e:
            raise TMDBError(f"Error getting popular movies: {str(e)}")

    def get_movie_recommendations(self, movie_id: int, page: int = 1, language: str = 'en-US') -> Dict:
        """Get movie recommendations based on a movie"""
        try:
            validate_movie_id(movie_id)
            validate_page_number(page)
            
            data = self._make_request(f"movie/{movie_id}/recommendations", {
                'page': page,
                'language': language
            })
            
            validate_response_data(data, ['results', 'page'])
            
            return {
                'page': data.get('page'),
                'total_pages': data.get('total_pages'),
                'total_results': data.get('total_results'),
                'movies': [self._format_movie(movie) for movie in data.get('results', [])]
            }
        except (TMDBAPIError, TMDBInvalidIDError) as e:
            raise
        except Exception as e:
            raise TMDBError(f"Error getting movie recommendations: {str(e)}") 