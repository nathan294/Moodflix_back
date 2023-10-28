import json

import requests
from fastapi import HTTPException


def search_in_tmdb(title: str, page: int = 1):
    # IMAGE_TMDB_ROUTE = "https://image.tmdb.org/t/p/original"
    API_KEY = "377e1f30f7462ca340230ce50a56d71b"
    HEADERS = {"accept": "application/json"}
    url = f"https://api.themoviedb.org/3/search/multi?query={title}&api_key={API_KEY}&include_adult=false&language=fr-FR&page={page}"

    # Make the request
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        response_content = response.content.decode("utf-8")  # Explicitly decode as UTF-8
        tmdb_data = json.loads(response_content)

        return tmdb_data
    else:
        raise HTTPException(response.status_code, response.reason)
