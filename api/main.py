import firebase_admin
from fastapi import FastAPI
from firebase_admin import credentials

from api.admin.router import router as admin_router
from api.movie.router import router as movie_router
from api.movie_list.router import router as movie_list_router

# Routers
from api.user.router import router as user_router

description = """
_Description in progress_ 🚀
"""

app = FastAPI(
    title="API de Moodflix",
    description=description,
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)


@app.on_event("startup")
def startup_event() -> None:
    cred = credentials.Certificate("/app/firebase_credentials.json")
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)


# Adds startup and shutdown events.
# register_startup_event(app)
# register_shutdown_event(app)
# register_exception_handlers(app)

app.include_router(admin_router)
app.include_router(user_router, prefix="/api")
app.include_router(movie_router, prefix="/api")
app.include_router(movie_list_router, prefix="/api")


@app.get("/")
def healthcheck():
    return "All good!"
