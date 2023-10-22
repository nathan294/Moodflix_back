from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from api.v1.models.rating import Rating


def user_rate_movie(movie_id: int, rating: int, user_id: str, db: Session) -> bool:
    """Movie rating by a specific user

    Args:
        movie_id (int): id of the movie
        rating (int): movie's rating according to the user
        user_id (str): user firebase id
        db (Session): sqlalchemy Session object
    """
    db_rating_dict = {"user_id": user_id, "movie_id": movie_id, "rating": rating}
    insert_stmt = insert(Rating)
    upsert_stmt = insert_stmt.on_conflict_do_update(
        index_elements=["user_id", "movie_id"],  # conflict target
        set_=dict(rating=insert_stmt.excluded.rating, updated_at=text("CURRENT_TIMESTAMP")),
    )
    # Execute the statement with the genres values
    db.execute(upsert_stmt, db_rating_dict)
    db.commit()
    return True
