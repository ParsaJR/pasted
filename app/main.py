import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from app.core import config
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core import logs
from app.routers import auth, management, pasted


@asynccontextmanager
async def lifespan(app: FastAPI):
    # db.create_db_and_tables()
    logs.setup_logger()
    yield


app = FastAPI(lifespan=lifespan)


#######################
# Logging middlewares #
#######################

logger = logs.get_logger()


@app.middleware("http")
async def log_process_time(request: Request, call_next):
    """It just logs requests for the sake of keeping track of the general performance results"""
    start_time = time.perf_counter()
    try:
        response = await call_next(request)
        return response
    finally:
        process_time = time.perf_counter() - start_time
        logger.info(
            f"{request.method} | {request.url.path} | request_completed ",
            extra={
                "tags": {
                    "http_method": request.method,
                    "path": request.url.path,
                    "process_time": round(process_time, 4),
                },
            },
        )


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    logger.error(
        f"{request.method} {exc.status_code} | {request.url.path}",
        extra={
            "tags": {
                "http_method": request.method,
                "path": request.url.path,
                "detail": repr(exc),
                "status_code": exc.status_code,
            },
        },
    )
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    status_code = 422

    logger.warning(
        f"{request.method} {status_code} | {request.url.path}",
        extra={
            "tags": {
                "http_method": request.method,
                "path": request.url.path,
                "detail": repr(exc),
                "status_code": status_code,
            },
        },
    )

    if not config.settings.env_development:
        return JSONResponse(
            status_code=422,
            content=jsonable_encoder(
                {"detail": "Invalid request. Please check the input and try again."}
            ),
        )

    return await request_validation_exception_handler(request, exc)


app.include_router(auth.router)
app.include_router(pasted.router)
app.include_router(management.router)
