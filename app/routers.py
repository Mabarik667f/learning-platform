from fastapi.routing import APIRouter
from users.router import router as user_router
from auth.router import router as auth_router

api_router = APIRouter()

api_router.include_router(user_router)
api_router.include_router(auth_router)
