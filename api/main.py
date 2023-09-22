from fastapi import FastAPI

from api.database import engine
from api.models import Base

# Routers
from api.routers import user
from api.settings import settings

description = """
_Description in progress_ 🚀
"""

app = FastAPI(title="API de Moodflix", description=description)
app.include_router(user.router)
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
