from fastapi import APIRouter

from api.v1.admin.router import router as admin_router
from api.v1.features.movie.router import router as movie_router
from api.v1.features.movie_list.router import router as movie_list_router
from api.v1.features.search.router import router as search_router
from api.v1.features.user.router import router as user_router
from api.v1.features.user_interaction.router import router as user_interaction_router

router = APIRouter(
    prefix="/v1",
    # tags=["v1"]
)

router.include_router(admin_router)
router.include_router(user_router)
router.include_router(movie_router)
router.include_router(movie_list_router)
router.include_router(user_interaction_router)
router.include_router(search_router)
