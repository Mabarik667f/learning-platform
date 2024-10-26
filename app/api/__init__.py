from fastapi.routing import APIRouter
from .users import router as user_router
from .auth import router as auth_router
from .categories import router as cat
from .courses import router as course_router
from .sections import router_section, router_subsection
from .tasks import router as task_router
from .submissions import router as subm_router

api_router = APIRouter()

api_router.include_router(user_router)
api_router.include_router(auth_router)
api_router.include_router(cat)
api_router.include_router(course_router)
api_router.include_router(router_section)
api_router.include_router(router_subsection)
api_router.include_router(task_router)
api_router.include_router(subm_router)
