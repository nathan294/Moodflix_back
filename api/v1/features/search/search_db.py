from itertools import chain
from typing import List

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from api.v1.features.movie.schemas import Movie
from api.v1.features.person.schemas import Person
from api.v1.features.search.schemas import TMDBResponse
from api.v1.models.movie import Movie as Movie_db
from api.v1.models.person import Person as Person_db


async def insert_into_database(tmdb_data: TMDBResponse, db: Session) -> bool:
    # Insert or update persons
    data = tmdb_data.get("results")
    # data = tmdb_data.results

    # try:
    # Retrieve movies
    movies = [movie for movie in data if isinstance(movie, Movie)]
    # Retrieve persons
    persons = [person for person in data if isinstance(person, Person)]

    # Retrieve persons' movies
    persons_movies = list(map(lambda x: x.movies, persons))
    # persons_movies = list(map(lambda x: x.get("movies"), persons))

    # Flatten the list of lists (persons_movies) and concatenate with movies
    all_movies = list(chain(movies, *persons_movies))

    insert_movies(all_movies, db)
    insert_persons(persons, db)


def insert_movies(movies: List[Movie], db: Session):
    # Create DB items
    db_movies = [movie.model_dump() for movie in movies]

    # Remove duplicates based on 'id'
    unique_movies = list({movie["id"]: movie for movie in db_movies}.values())

    # Create an insert statement for the Movie table
    insert_stmt = insert(Movie_db).values(unique_movies)

    # Add the on conflict do update clause
    final_stmt = insert_stmt.on_conflict_do_update(
        index_elements=["id"],  # conflict target
        set_=dict(
            title=insert_stmt.excluded.title,
            overview=insert_stmt.excluded.overview,
            popularity=insert_stmt.excluded.popularity,
            vote_average=insert_stmt.excluded.vote_average,
            vote_count=insert_stmt.excluded.vote_count,
        ),
    )

    # Execute the statement
    db.execute(final_stmt)
    db.commit()
    return True


def insert_persons(persons: List[Person], db: Session):
    # Create DB items
    db_persons = []
    for person in persons:
        person_dict = person.model_dump()
        # Replace 'movies' with just a list of movie IDs
        person_dict["movie_ids"] = [movie.id for movie in person.movies]
        del person_dict["movies"]
        db_persons.append(person_dict)

    # Remove duplicates based on 'id'
    unique_persons = list({person["id"]: person for person in db_persons}.values())

    # Create an insert statement for the Movie table
    insert_stmt = insert(Person_db).values(unique_persons)

    # Add the on conflict do update clause
    final_stmt = insert_stmt.on_conflict_do_update(
        index_elements=["id"],  # conflict target
        set_=dict(
            movie_ids=insert_stmt.excluded.movie_ids,
        ),
    )

    # Execute the statement
    db.execute(final_stmt)
    db.commit()
    return True
