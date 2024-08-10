import sys

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi import Request
from starlette.routing import Match

from routers import api_router
from core.config import settings
from loguru import logger

logger.remove()

# requests logger
logger.add(sys.stdout, colorize=True, format="<green>{time:HH:mm:ss}</green> | {level} | <level>{message}</level>",
    level="DEBUG")

# add loggers:
logger.add("logging/debugger.log", colorize=True, rotation="10 KB", level="INFO",
    format="{time:HH:mm:ss} | {level} | {message}",
    compression="zip")


app = FastAPI()

app.include_router(api_router)

if settings.BACKEND_CORS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            origin for origin in settings.BACKEND_CORS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

@app.middleware("http")
async def log_middleware(request: Request, call_next):
    logger.debug(f"{request.method} {request.url}")
    routes = request.app.router.routes
    logger.debug("Params:")
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
