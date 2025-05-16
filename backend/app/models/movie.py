from typing import List, Optional
from pydantic import BaseModel, Field

class Genre(BaseModel):
    id: int
    name: str

class ProductionCompany(BaseModel):
    id: int
    name: str

class MovieBase(BaseModel):
    id: int
    title: str
    overview: Optional[str] = None
    poster_url: Optional[str] = None
    backdrop_url: Optional[str] = None
    release_date: Optional[str] = None
    rating: Optional[float] = Field(None, alias="vote_average")
    genres: List[int] = Field(default_factory=list)

class MovieDetail(MovieBase):
    tagline: Optional[str] = None
    runtime: Optional[int] = None
    budget: Optional[int] = None
    revenue: Optional[int] = None
    genres: List[Genre] = Field(default_factory=list)
    production_companies: List[ProductionCompany] = Field(default_factory=list)
    status: Optional[str] = None
    original_language: Optional[str] = None

class MovieSearchResponse(BaseModel):
    page: int
    total_pages: int
    total_results: int
    movies: List[MovieBase]

class MovieRecommendationResponse(BaseModel):
    page: int
    total_pages: int
    total_results: int
    movies: List[MovieBase] 