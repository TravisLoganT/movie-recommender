from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from ..models.movie import MovieDetail, MovieSearchResponse, MovieRecommendationResponse
from ..utils.tmdb_client import TMDBClient
from ..core.config import get_settings

router = APIRouter(prefix="/movies", tags=["movies"])

def get_tmdb_client() -> TMDBClient:
    """Dependency to get TMDB client instance"""
    settings = get_settings()
    return TMDBClient(settings.tmdb_api_key)

@router.get("/search", response_model=MovieSearchResponse)
async def search_movies(
    query: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    language: str = Query("en-US", min_length=2, max_length=5),
    client: TMDBClient = Depends(get_tmdb_client)
):
    """Search for movies"""
    try:
        result = client.search_movies(query, page, language)
        return MovieSearchResponse(
            page=result["page"],
            total_pages=result["total_pages"],
            total_results=result["total_results"],
            movies=result["movies"]
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{movie_id}", response_model=MovieDetail)
async def get_movie_details(
    movie_id: int,
    language: str = Query("en-US", min_length=2, max_length=5),
    client: TMDBClient = Depends(get_tmdb_client)
):
    """Get detailed information about a specific movie"""
    try:
        return client.get_movie_details(movie_id, language)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/popular", response_model=MovieSearchResponse)
async def get_popular_movies(
    page: int = Query(1, ge=1),
    language: str = Query("en-US", min_length=2, max_length=5),
    client: TMDBClient = Depends(get_tmdb_client)
):
    """Get popular movies"""
    try:
        result = client.get_popular_movies(page, language)
        return MovieSearchResponse(
            page=result["page"],
            total_pages=result["total_pages"],
            total_results=result["total_results"],
            movies=result["movies"]
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{movie_id}/recommendations", response_model=MovieRecommendationResponse)
async def get_movie_recommendations(
    movie_id: int,
    page: int = Query(1, ge=1),
    language: str = Query("en-US", min_length=2, max_length=5),
    client: TMDBClient = Depends(get_tmdb_client)
):
    """Get movie recommendations based on a movie"""
    try:
        result = client.get_movie_recommendations(movie_id, page, language)
        return MovieRecommendationResponse(
            page=result["page"],
            total_pages=result["total_pages"],
            total_results=result["total_results"],
            movies=result["movies"]
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 