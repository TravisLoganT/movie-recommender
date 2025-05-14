import os
import requests

class TMBDClient:
    def __init__(self, api_key: str) -> None:
        self.url = 'https://api.themoviedb.org/3/'
        self.params = {
            'api_key': api_key
        }

    def _format_movie(self, movie: dict) -> dict:
        return {
            'id': movie.get('id'),
            'title': movie.get('title'),
            'overview': movie.get('overview'),
            'poster_url': f"https://image.tmdb.org/t/p/w500{movie.get('poster_url')}" if movie.get('poster_path') else None,
            'release_date': movie.get('release_date'),
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