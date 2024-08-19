from fastapi.routing import APIRouter
from core.deps import SessionDep


router = APIRouter(tags=['courses'], prefix='/courses')
