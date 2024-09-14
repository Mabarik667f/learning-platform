from fastapi import Depends
from typing import Annotated
from models.users import User
from auth.crud import get_current_active_user

CurActiveUserDep = Annotated[User, Depends(get_current_active_user)]
