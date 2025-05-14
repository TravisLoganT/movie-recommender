import requests
from typing import Dict, Any

class TMDBError(Exception):
    """Base exception for TMDB API errors"""
    pass

class TMDBAPIError(TMDBError):
    """Exception for API-related errors"""
    pass

class TMDBInvalidIDError(TMDBError):
    """Exception for invalid movie ID"""
    pass

class TMDBInvalidQueryError(TMDBError):
    """Exception for invalid search query"""
    pass

def handle_api_response(response: requests.Response) -> None:
    """Handle common API response errors"""
    if response.status_code == 401:
        raise TMDBAPIError("Invalid API key")
    elif response.status_code == 404:
        raise TMDBAPIError("Resource not found")
    elif response.status_code >= 500:
        raise TMDBAPIError("TMDB API server error")
    elif response.status_code >= 400:
        raise TMDBAPIError(f"API error: {response.status_code}")

def validate_movie_id(movie_id: int) -> None:
    """Validate movie ID"""
    if not isinstance(movie_id, int) or movie_id <= 0:
        raise TMDBInvalidIDError("Movie ID must be a positive integer")

def validate_search_query(query: str) -> None:
    """Validate search query"""
    if not query or not isinstance(query, str):
        raise TMDBInvalidQueryError("Search query must be a non-empty string")

def validate_page_number(page: int) -> None:
    """Validate page number"""
    if not isinstance(page, int) or page < 1:
        raise ValueError("Page number must be a positive integer")

def validate_response_data(data: dict, required_fields: list) -> None:
    """Validate response data has required fields"""
    if not isinstance(data, dict):
        raise TMDBAPIError("Invalid response format")
    
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise TMDBAPIError(f"Missing required fields: {', '.join(missing_fields)}")
    