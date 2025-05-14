import pytest
from unittest.mock import Mock, patch
from app.utils.tmdb_client import TMDBClient
from app.utils.error_handlers import (
    TMDBError,
    TMDBAPIError,
    TMDBInvalidIDError,
    TMDBInvalidQueryError
)
import requests

# Sample test data
SAMPLE_MOVIE = {
    'id': 27205,
    'title': 'Inception',
    'overview': 'A thief who steals corporate secrets...',
    'poster_path': '/poster.jpg',
    'backdrop_path': '/backdrop.jpg',
    'release_date': '2010-07-15',
    'vote_average': 8.4,
    'genre_ids': [28, 878],
    'tagline': 'Your mind is the scene of the crime.',
    'runtime': 148,
    'budget': 160000000,
    'revenue': 836836967,
    'genres': [{'id': 28, 'name': 'Action'}, {'id': 878, 'name': 'Science Fiction'}],
    'production_companies': [{'id': 1, 'name': 'Warner Bros.'}],
    'status': 'Released',
    'original_language': 'en'
}

SAMPLE_SEARCH_RESPONSE = {
    'page': 1,
    'results': [SAMPLE_MOVIE],
    'total_pages': 1,
    'total_results': 1
}

@pytest.fixture
def client():
    """Create a TMDB client instance for testing"""
    return TMDBClient('test_api_key')

@pytest.fixture
def mock_response():
    """Create a mock response object"""
    mock = Mock()
    mock.status_code = 200
    mock.json.return_value = SAMPLE_SEARCH_RESPONSE
    return mock

def test_init(client):
    """Test client initialization"""
    assert client.base_url == 'https://api.themoviedb.org/3/'
    assert client.params == {'api_key': 'test_api_key'}

@patch('requests.get')
def test_search_movies(mock_get, client, mock_response):
    """Test movie search functionality"""
    mock_get.return_value = mock_response
    
    result = client.search_movies("Inception")
    
    assert result['page'] == 1
    assert len(result['movies']) == 1
    assert result['movies'][0]['title'] == 'Inception'
    mock_get.assert_called_once()

@patch('requests.get')
def test_get_movie_details(mock_get, client, mock_response):
    """Test getting movie details"""
    mock_response.json.return_value = SAMPLE_MOVIE
    mock_get.return_value = mock_response
    
    result = client.get_movie_details(27205)
    
    assert result['title'] == 'Inception'
    assert result['runtime'] == 148
    assert result['genres'][0]['name'] == 'Action'
    mock_get.assert_called_once()

@patch('requests.get')
def test_get_popular_movies(mock_get, client, mock_response):
    """Test getting popular movies"""
    mock_get.return_value = mock_response
    
    result = client.get_popular_movies()
    
    assert result['page'] == 1
    assert len(result['movies']) == 1
    assert result['movies'][0]['title'] == 'Inception'
    mock_get.assert_called_once()

@patch('requests.get')
def test_get_movie_recommendations(mock_get, client, mock_response):
    """Test getting movie recommendations"""
    mock_get.return_value = mock_response
    
    result = client.get_movie_recommendations(27205)
    
    assert result['page'] == 1
    assert len(result['movies']) == 1
    assert result['movies'][0]['title'] == 'Inception'
    mock_get.assert_called_once()

def test_invalid_movie_id(client):
    """Test error handling for invalid movie ID"""
    with pytest.raises(TMDBInvalidIDError):
        client.get_movie_details(-1)

def test_invalid_search_query(client):
    """Test error handling for invalid search query"""
    with pytest.raises(TMDBInvalidQueryError):
        client.search_movies("")

@patch('requests.get')
def test_api_error_handling(mock_get, client):
    """Test API error handling"""
    mock_response = Mock()
    mock_response.status_code = 401
    mock_get.return_value = mock_response
    
    with pytest.raises(TMDBAPIError):
        client.search_movies("Inception")

@patch('requests.get')
def test_network_error_handling(mock_get, client):
    """Test network error handling"""
    mock_get.side_effect = requests.exceptions.RequestException("Network error")
    
    with pytest.raises(TMDBAPIError):
        client.search_movies("Inception") 