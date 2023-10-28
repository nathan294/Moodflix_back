import json
from typing import Dict, List

import requests
from fastapi import HTTPException

import api.v1.features.movie.schemas as sch


def search_movie_in_tmdb_api(title: str) -> List[sch.Movie]:
    """
    Search for movie in TMDB API, return a list of movies
    """
    image_tmdb_route = "https://image.tmdb.org/t/p/original"
    api_key = "377e1f30f7462ca340230ce50a56d71b"
    headers = {"accept": "application/json"}
    all_movies_data = []

    for page in [1, 2]:
        url = f"https://api.themoviedb.org/3/search/multi?query={title}&api_key={api_key}&include_adult=false&language=fr-FR&page={page}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response_content = response.content.decode("utf-8")  # Explicitly decode as UTF-8
            data = json.loads(response_content)
            movies_data = data.get("results", [])
            all_movies_data.extend(movies_data)  # Concatenate the results

        # Create a list of Movie objects and set release_year field
        movies = []
        for movie_data in all_movies_data:
            try:
                # Movies & TV Show response differ
                release_date = movie_data.get("release_date") or movie_data.get("first_air_date")
                title = movie_data.get("title") or movie_data.get("name")
                original_title = movie_data.get("original_title") or movie_data.get("original_name")

                # Convert empty string to None
                release_date = None if release_date == "" else release_date

                media_type = movie_data.get("media_type")
                poster_path = movie_data.get("poster_path")
                backdrop_path = movie_data.get("backdrop_path")
                if media_type == "person" or any(x is None for x in [poster_path, backdrop_path, title, release_date]):
                    continue  # Skip this row and continue with the next one

                # Create a pydantic Movie from the response
                if title is not None and release_date is not None:
                    movie = sch.Movie(
                        id=movie_data.get("id"),
                        title=title,
                        type=media_type,
                        genre_ids=movie_data.get("genre_ids"),
                        original_language=movie_data.get("original_language"),
                        original_title=original_title,
                        overview=movie_data.get("overview"),
                        poster_path=(image_tmdb_route + poster_path),
                        backdrop_path=(image_tmdb_route + backdrop_path),
                        release_date=release_date,
                        release_year=None,
                        popularity=movie_data.get("popularity"),
                        vote_average=movie_data.get("vote_average"),
                        vote_count=movie_data.get("vote_count"),
                    )
                    # Extract year from release_date and set it to release_year
                    movie.release_year = movie.release_date.year
                    movies.append(movie)
            except Exception as e:
                print(f"An error occurred while processing a movie: {e}")
                continue  # Skip this movie and continue with the next one

        return movies
    else:
        return HTTPException(400, "An unexpected error occured")


def get_genres_from_tmdb(media_type: str) -> List[Dict]:
    """
    Get genres id & names from TMDB API
    """
    api_key = "377e1f30f7462ca340230ce50a56d71b"
    url = f"https://api.themoviedb.org/3/genre/{media_type}/list?api_key={api_key}&language=fr-FR"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_content = response.content.decode("utf-8")
        data = json.loads(response_content)
        genres = data.get("genres", [])
        return genres
    else:
        return []


def get_list_from_tmdb(wanted_list: sch.WantedList) -> List[sch.Movie]:
    """
    Get list from TMDB API
    * Now Playing : To get movies in theaters, use _now\_playing_
    * Popular : To get popular movies, use _popular_
    * Top Rated : To get top rated movies, use _top\_rated_
    * Upcoming : To get upcoming movies, use _upcoming_
    """
    image_tmdb_route = "https://image.tmdb.org/t/p/original"
    api_key = "377e1f30f7462ca340230ce50a56d71b"
    headers = {"accept": "application/json"}
    all_movies_data = []

    for page in [1, 2]:
        url = f"https://api.themoviedb.org/3/movie/{wanted_list.value}?api_key={api_key}&include_adult=false&language=fr-FR&page={page}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response_content = response.content.decode("utf-8")  # Explicitly decode as UTF-8
            data = json.loads(response_content)
            movies_data = data.get("results", [])
            all_movies_data.extend(movies_data)  # Concatenate the results
        else:
            raise HTTPException(status_code=response.status_code, detail=response.reason)
        # Create a list of Movie objects and set release_year field
        movies = []
        for movie_data in all_movies_data:
            try:
                # Movies & TV Show response differ
                release_date = movie_data.get("release_date")
                title = movie_data.get("title")
                original_title = movie_data.get("original_title")

                # Convert empty string to None
                release_date = None if release_date == "" else release_date

                poster_path = movie_data.get("poster_path")
                backdrop_path = movie_data.get("backdrop_path")

                # Create a pydantic Movie from the response
                if title is not None and release_date is not None:
                    movie = sch.Movie(
                        id=movie_data.get("id"),
                        title=title,
                        type="movie",  # Only movies here
                        genre_ids=movie_data.get("genre_ids"),
                        original_language=movie_data.get("original_language"),
                        original_title=original_title,
                        overview=movie_data.get("overview"),
                        poster_path=(image_tmdb_route + poster_path),
                        backdrop_path=(image_tmdb_route + backdrop_path),
                        release_date=release_date,
                        release_year=None,
                        popularity=movie_data.get("popularity"),
                        vote_average=movie_data.get("vote_average"),
                        vote_count=movie_data.get("vote_count"),
                    )
                    # Extract year from release_date and set it to release_year
                    movie.release_year = movie.release_date.year
                    movies.append(movie)
            except Exception as e:
                print(f"An error occurred while processing a movie: {e}")
                continue  # Skip this movie and continue with the next one

        return movies
    else:
        return HTTPException(400, "An unexpected error occured")
