from typing import Annotated, Any

from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from fastapi.responses import Response
from fastapi.routing import APIRouter
from fastapi import status

from users import crud
from users.shemas import User, UserAllData, UserCreate, UserResponse, UserUpdate

from .deps import CurActiveUserDep
from core.deps import SessionDep
from core.config import settings

from loguru import logger


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def me(current_user: CurActiveUserDep):
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(session: SessionDep, user_id: int):
    user = await crud.get_user_by_id(session, user_id)
    return UserResponse(**user.to_dict())


@router.post("/create-user", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(session: SessionDep, user: UserCreate) -> Any:
    user_obj = await crud.create_user(session=session, user=user)
    return User(**user_obj.to_dict())


@router.delete("/delete-user/{user_id}")
async def delete_user(session: SessionDep, user_id: int) -> Response:
    await crud.delete_user(session=session, user_id=user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/update-data/{user_id}", response_model=UserAllData)
async def update_user_data(session: SessionDep, user_id: int, user: UserUpdate):
    user_obj = await crud.update_user_data(session, user_id, user)
    return UserAllData(**user_obj.to_dict())
