import firebase_admin
from fastapi import FastAPI
from firebase_admin import credentials


def register_startup_event(app: FastAPI):
    """Actions to run on app startup.

    This function uses fastAPI app to store data
    inthe state, such as db_engine.

    :param app: the fastAPI app.
    :return: function that actually performs actions.
    """

    @app.on_event("startup")
    async def startup_event() -> None:
        cred = credentials.Certificate("/app/firebase_credentials.json")
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)


def register_shutdown_event(app: FastAPI):
    """Actions to run on app's shutdown.

    :param app: fastAPI app.
    :return: function that actually performs actions.
    """

    @app.on_event("shutdown")
    async def shutdown_event() -> None:
        pass
