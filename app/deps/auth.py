from fastapi import Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer
from passlib.context import CryptContext

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token", scopes={"me": "about me"})
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

OAuth2Dep = Depends(oauth2_scheme)
