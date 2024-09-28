from fastapi.routing import APIRouter
from users.router import router as user_router
from auth.router import router as auth_router
from categories.router import router as cat
from courses.router import router as course_router
from sections.router import router_section, router_subsection

api_router = APIRouter()

api_router.include_router(user_router)

api_router.include_router(auth_router)

api_router.include_router(cat)
api_router.include_router(course_router)

api_router.include_router(router_section)
api_router.include_router(router_subsection)
