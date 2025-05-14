import os
from dotenv import load_dotenv
from app.utils.tmdb_client import TMDBClient
from app.utils.error_handlers import TMDBError, TMDBAPIError, TMDBInvalidIDError

def main():
    # Load environment variables
    load_dotenv()
    api_key = os.getenv('TMBD_API_KEY')

    # Initialize client
    client = TMDBClient(api_key)

    try:
        # Test search
        print("\nSearching for 'Inception':")
        search_results = client.search_movies("Inception")
        print(search_results)

        # Test movie details
        print("\nGetting details for Inception (ID: 27205):")
        movie_details = client.get_movie_details(27205)
        print(movie_details)

        # Test popular movies
        print("\nGetting popular movies:")
        popular_movies = client.get_popular_movies()
        print(popular_movies)

        # Test recommendations
        print("\nGetting recommendations for Inception:")
        recommendations = client.get_movie_recommendations(27205)
        print(recommendations)

    except TMDBInvalidIDError as e:
        print(f"Invalid ID error: {e}")
    except TMDBAPIError as e:
        print(f"API error: {e}")
    except TMDBError as e:
        print(f"General error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()