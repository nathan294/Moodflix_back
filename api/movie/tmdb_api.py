import json
from typing import List

import requests
from fastapi import HTTPException

import api.movie.schemas as sch


def search_movie_in_tmdb_api(title: str) -> List[sch.MovieCreate]:
    image_tmdb_route = "https://image.tmdb.org/t/p/original"
    api_key = "377e1f30f7462ca340230ce50a56d71b"
    url = (
        f"https://api.themoviedb.org/3/search/movie?query={title}&api_key={api_key}&include_adult=false&language=fr-FR"
    )
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_content = response.content.decode("utf-8")  # Explicitly decode as UTF-8
        data = json.loads(response_content)
        movies_data = data.get("results", [])

        # Create a list of MovieCreate objects and set release_year field
        movies = []
        for movie_data in movies_data:
            try:
                release_date = movie_data.get("release_date")
                # Convert empty string to None
                release_date = None if release_date == "" else release_date

                # Create a pydantic Movie from the response
                # Add None if there is no poster_path or backdrop_path
                movie = sch.MovieCreate(
                    id=movie_data.get("id"),
                    title=movie_data.get("title"),
                    genre_ids=movie_data.get("genre_ids"),
                    original_language=movie_data.get("original_language"),
                    original_title=movie_data.get("original_title"),
                    overview=movie_data.get("overview"),
                    poster_path=(image_tmdb_route + movie_data.get("poster_path"))
                    if movie_data.get("poster_path")
                    else None,
                    backdrop_path=(image_tmdb_route + movie_data.get("backdrop_path"))
                    if movie_data.get("backdrop_path")
                    else None,
                    release_date=movie_data.get("release_date"),
                    release_year=None,
                    popularity=movie_data.get("popularity"),
                    vote_average=movie_data.get("vote_average"),
                    vote_count=movie_data.get("vote_count"),
                )
                # Extract year from release_date and set it to release_year
                if movie.release_date:
                    movie.release_year = movie.release_date.year
                movies.append(movie)
            except Exception as e:
                print(f"An error occurred while processing a movie: {e}")
                continue  # Skip this movie and continue with the next one

        return movies
    else:
        return HTTPException(400, "Une erreur est survenue lors de la récupération des films")