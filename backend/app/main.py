from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import movies, users

app = FastAPI(
    title="Movie Recommender API",
    description="API for movie recommendations and information",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(movies.router)
app.include_router(users.router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Movie Recommender API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }
