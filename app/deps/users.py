from fastapi import Depends
from typing import Annotated
from crud.auth import get_current_active_user
from models.users import User

CurActiveUserDep = Annotated[User, Depends(get_current_active_user)]
