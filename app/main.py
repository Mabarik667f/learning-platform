import asyncio
from contextlib import asynccontextmanager
import sys

from fastapi import FastAPI, Response, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from fastapi import Request
from starlette.routing import Match

from deps.users import CurActiveUserDep
from rabbit.get_result import get_submission_result
from rabbit.consumer_submissions import run_submissions_consumer
from core.exceptions import CoreValidationError
from api import api_router
from core.config import settings
from loguru import logger

logger.remove()

# requests logger
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:HH:mm:ss}</green> | {level} | <level>{message}</level>",
    level="DEBUG",
)

# add loggers:
logger.add(
    "logging/debugger.log",
    colorize=True,
    rotation="10 KB",
    level="INFO",
    format="{time:HH:mm:ss} | {level} | {message}",
    compression="zip",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(run_submissions_consumer())
    try:
        yield
    finally:
        task.cancel()


app = FastAPI(lifespan=lifespan)

app.include_router(api_router)
# app.mount("/media", StaticFiles(directory="media"), name="media")

if settings.BACKEND_CORS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[origin for origin in settings.BACKEND_CORS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.middleware("http")
async def log_middleware(request: Request, call_next):
    if settings.REQUESTS_LOGGIN_MIDDLEWARE:
        logger.debug(f"{request.method} {request.url}")
        routes = request.app.router.routes
        for route in routes:
            match, scope = route.matches(request)
            if match == Match.FULL:
                for name, val in scope["path_params"].items():
                    logger.debug(f"\t{name}: {val}")

        logger.debug("Headers:")
        for name, val in request.headers.items():
            logger.debug(f"\t{name}: {val}")

    response = await call_next(request)
    return response


@app.exception_handler(CoreValidationError)
def core_validation_exc_handler(request, exc: CoreValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"detail": exc.to_dict()}
    )
