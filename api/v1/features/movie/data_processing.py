from typing import Dict, List

import api.v1.features.movie.schemas as sch


def concatenate_genres(movie_genres: List[Dict], tv_genres: List[Dict]) -> List[Dict]:
    """
    Concatenate movies & TV show genre names
    """
    concatenated = {}
    for genre in movie_genres + tv_genres:
        genre_id = genre["id"]
        genre_name = genre["name"]
        concatenated[genre_id] = genre_name
    return [{"id": k, "name": v} for k, v in concatenated.items()]


def concatenate_home_lists(
    popular_movies: List[sch.Movie],
    now_playing_movies: List[sch.Movie],
    upcoming_movies: List[sch.Movie],
):
    return {"popular": popular_movies, "now_playing": now_playing_movies, "upcoming": upcoming_movies}
