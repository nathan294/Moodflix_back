import firebase_admin
from fastapi import FastAPI
from firebase_admin import credentials

from api.v1.router import router as v1_router

description = """
_Description in progress_ 🚀
"""

app = FastAPI(
    title="API de Moodflix",
    description=description,
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.v1.json",
    prefix="/api",
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

# Include V1 Router
app.include_router(v1_router)


@app.get("/")
def healthcheck():
    return "All good!"
