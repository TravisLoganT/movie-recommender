import os
import requests

class TMBDClient:
    def __init__(self, api_key: str) -> None:
        self.url = 'https://api.themoviedb.org/3/'
        self.params = {
            'api_key': api_key
        }

    def _format_movie(self, movie: dict) -> dict:
        poster_path = movie.get('poster_path')
        return {
            'id': movie.get('id'),
            'title': movie.get('title'),
            'overview': movie.get('overview'),
            'poster_url': f"https://image.tmdb.org/t/p/w500{poster_path}",
            'release_date': movie.get('release_date') or None,
            'rating': movie.get('vote_average'),
            'genres':movie.get('genre_ids', [])

        }

    def search_movies(self, query: str, page: int = 1, language: str = 'en-US') -> dict:
        search_params = {
            **self.params,
            'query': query,
            'page': page,
            'language': language
        }
        endpoint = f"{self.url}search/movie"

        response = requests.get(endpoint, params=search_params)
        response.raise_for_status()

        data = response.json()
        return {
            'page': data.get('page'),
            'total_pages': data.get('total_pages'),
            'total_results': data.get('toal_results'),
            'movies': [self._format_movie(movie) for movie in data.get('results', [])]
        }
    
    def get_movie_details(self, movie_id: int, language: str = 'en-US') -> dict:
        search_params = {
            **self.params,
            'movie_id': movie_id,
            'language': language
        }
        endpoint = f'{self.url}movie/{movie_id}'

        response = requests.get(endpoint, params=search_params)
        response.raise_for_status()

        data = response.json()
        return {
            'title': data.get('original_title'),
            'tagline': data.get('tagline'),
            'overview': data.get('overview'),
            'release_date': data.get('release_date') or None,
            'genres': [{g['name']} for g in data.get('genres', [])],
            'rating': data.get('vote_average'),
            'runtime': data.get('runtime'),
            'original_language': data.get('original_language')
        }