import requests
from typing import Dict, Any

class TMDBError(Exception):
    """Base exception for TMDB API errors"""
    pass

class TMDBAPIError(TMDBError):
    """Exception for API-specific errors"""
    pass

class TMDBInvalidIDError(TMDBError):
    """Exception for invalid movie IDs"""
    pass

def handle_api_response(response: requests.Response) -> None:
    """Handle common API response errors"""
    if response.status_code == 401:
        raise TMDBAPIError("Invalid API key")
    elif response.status_code == 404:
        raise TMDBInvalidIDError("Resource not found")
    elif response.status_code == 429:
        raise TMDBAPIError("Rate limit exceeded")
    elif response.status_code != 200:
        raise TMDBAPIError(f"API request failed with status {response.status_code}")

def validate_movie_id(movie_id: int) -> None:
    """Validate movie ID"""
    if not isinstance(movie_id, int) or movie_id <= 0:
        raise ValueError("Movie ID must be a positive integer")

def validate_search_query(query: str) -> None:
    """Validate search query"""
    if not query or not isinstance(query, str):
        raise ValueError("Search query must be a non-empty string")

def validate_page_number(page: int) -> None:
    """Validate page number"""
    if not isinstance(page, int) or page < 1:
        raise ValueError("Page must be a positive integer")

def validate_response_data(data: Dict[str, Any], required_fields: list) -> None:
    """Validate response data structure"""
    if not data:
        raise TMDBAPIError("Empty response from API")
    for field in required_fields:
        if field not in data:
            raise TMDBAPIError(f"Missing required field: {field}")
    