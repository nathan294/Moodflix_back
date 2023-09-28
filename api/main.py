from fastapi import FastAPI

from api.database import engine
from api.models import Base
from api.movie.router import router as movie_router
from api.settings import settings

# Routers
from api.user.router import router as user_router

description = """
_Description in progress_ 🚀
"""

app = FastAPI(title="API de Moodflix", description=description)
app.include_router(user_router)
app.include_router(movie_router)
Base.metadata.create_all(bind=engine)


@app.get("/")
def healthcheck():
    return "All good!"


@app.get("/route_hyper_secure")
def tester_la_securite():
    return {
        "DB_HOST": settings.DB_HOST,
        "DB_USER": settings.DB_USER,
        "DB_PASS": settings.DB_PASS,
        "DB_NAME": settings.DB_NAME,
        "DB_PORT": settings.DB_PORT,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="debug", reload="true")
    uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="debug", reload="true")
