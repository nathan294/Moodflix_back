"""Template App
"""
import logging

from fastapi import FastAPI, Request, status
from fastapi.v1.responses import JSONResponse
from sqlalchemy.exc import IntegrityError


async def sqlalchemy_integrity_error_handler(_: Request, exception: IntegrityError) -> JSONResponse:
    """High level exception handler for all exceptions"""
    logging.exception(exception)
    return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"message": "Resource Already Exists"})


async def default_error_handler(_: Request, exception: Exception) -> JSONResponse:
    """High level exception handler for all exceptions"""
    logging.exception(exception)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Unhandled Internal Server Error"}
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Add exception handlers to FastAPI app"""
    app.add_exception_handler(IntegrityError, sqlalchemy_integrity_error_handler)
    app.add_exception_handler(Exception, default_error_handler)
