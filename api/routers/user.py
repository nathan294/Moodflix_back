from fastapi import APIRouter

router = APIRouter(
    prefix="/user",
    tags=["User"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def healthcheck():
    return "All good!"
