from typing import Dict, List


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
