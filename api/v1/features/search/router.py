from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from api.v1.commons.dependencies import get_db
from api.v1.features.search.data_cleaning import clean_tmdb_data
from api.v1.features.search.schemas import TMDBResponse
from api.v1.features.search.search_db import insert_into_database

# from fastapi.responses import StreamingResponse
from api.v1.features.search.tmdb_api import search_in_tmdb

router = APIRouter(
    prefix="/search",
    tags=["Search"],
)


@router.get("/", response_model=TMDBResponse)
async def search_multi(title: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    tmdb_data = search_in_tmdb(title)
    clean_data = clean_tmdb_data(tmdb_data)

    background_tasks.add_task(insert_into_database, clean_data, db)
    return clean_data
