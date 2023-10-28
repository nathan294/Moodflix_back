from fastapi import APIRouter

from api.v1.features.person.person_db import get_person_db

router = APIRouter(
    prefix="/person",
    tags=["Person"],
)


@router.get("/")
async def get_person():
    """Get a person (film director, actor...)"""
    return get_person_db()
