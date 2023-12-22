from typing import Dict

from api.v1.commons.enums.gender import Gender
from api.v1.features.movie.schemas import Movie
from api.v1.features.person.schemas import Person
from api.v1.features.search.schemas import TMDBResponse

IMAGE_TMDB_ROUTE = "https://image.tmdb.org/t/p/original"


def clean_tmdb_data(tmdb_data: Dict) -> TMDBResponse:
    all_data = tmdb_data.get("results", [])

    # We need to filter for incorrect data to enhance the quality
    correct_data = []

    # Loop into all our items
    for item in all_data:
        if (item.get("media_type") == "movie") | (item.get("media_type") == "tv"):
            # Item is a movie or a tv show
            movie = clean_movie_or_tv_show_data(item)
            if movie:
                correct_data.append(movie)

        elif item.get("media_type") == "person":
            # Item is a person
            person = clean_person_data(item)
            if person:
                correct_data.append(person)

        else:
            # Don't get this object into account
            continue

    page = tmdb_data.get("page", [])
    total_pages = tmdb_data.get("total_pages", [])

    return {"page": page, "total_pages": total_pages, "results": correct_data}


def clean_movie_or_tv_show_data(item) -> Movie | None:
    """Clean Movies and TV Shows data from TMDB"""

    # Movies & TV Show response differ
    release_date = item.get("release_date") or item.get("first_air_date")
    title = item.get("title") or item.get("name")
    original_title = item.get("original_title") or item.get("original_name")

    # Convert empty string to None
    release_date = None if release_date == "" else release_date

    media_type = item.get("media_type")
    poster_path = item.get("poster_path")
    backdrop_path = item.get("backdrop_path")
    if any(x is None for x in [poster_path, backdrop_path, title, release_date]):
        return  # Skip this item and continue with the next one

    # Create a pydantic Movie from the response
    if title is not None and release_date is not None:
        movie = Movie(
            id=item.get("id"),
            title=title,
            type=media_type,
            genre_ids=item.get("genre_ids"),
            original_language=item.get("original_language"),
            original_title=original_title,
            overview=item.get("overview"),
            poster_path=(IMAGE_TMDB_ROUTE + poster_path),
            backdrop_path=(IMAGE_TMDB_ROUTE + backdrop_path),
            release_date=release_date,
            release_year=None,
            popularity=item.get("popularity"),
            vote_average=item.get("vote_average"),
            vote_count=item.get("vote_count"),
        )
        # Extract year from release_date and set it to release_year
        movie.release_year = movie.release_date.year

        return movie


def clean_person_data(item) -> Person | None:
    department = item.get("known_for_department")
    job = get_person_job(department)
    gender = get_person_gender(item.get("gender"))

    name = item.get("name")
    profile_path = item.get("profile_path")

    if any(x is None for x in [name, job, profile_path]):
        return  # Skip this item and continue with the next one

    # Get & clean person movies
    person_movies = item.get("known_for")
    person_correct_movies = []
    if person_movies:
        for item in person_movies:
            movie = clean_movie_or_tv_show_data(item)
            if movie:
                person_correct_movies.append(movie)

    person = Person(
        id=item.get("id"),
        name=name,
        original_name=item.get("original_name"),
        gender=gender,
        job=job,
        profile_path=(IMAGE_TMDB_ROUTE + profile_path),
        movies=person_correct_movies,
    )

    return person


def get_person_job(department: str) -> str:
    if department == "Acting":
        return "Acteur"
    elif department == "Directing":
        return "Réalisateur"
    elif department == "Production":
        return "Producteur"


def get_person_gender(gender: int) -> Gender:
    if gender == 2:
        return Gender.male
    elif gender == 1:
        return Gender.female
    else:
        return Gender.other
