import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('TMBD_API_KEY')

params = {
    'api_key': api_key
}

response = requests.get('https://api.themoviedb.org/3/movie/popular', params=params)

print(response.json())