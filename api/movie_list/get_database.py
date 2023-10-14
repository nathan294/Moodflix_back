from typing import List

from sqlalchemy import case, desc, select
from sqlalchemy.orm import Session

from api.models.movie_list import MovieList


def get_movie_lists_for_user(user_id: str, db: Session) -> List[MovieList]:
    stmt = (
        select(MovieList)
        .filter_by(user_id=user_id)
        .order_by(case((MovieList.locked == True, 1), else_=0).desc(), desc(MovieList.created_at))
    )
    movie_lists = db.execute(stmt).scalars().all()
    return movie_lists
