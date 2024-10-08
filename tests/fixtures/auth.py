import pytest
from tests.helpers.auth_utils import BearerAuth
from main import app  # type: ignore

default_user_data: dict = {
    "email": "aboba@gmail.com",
    "username": "Test",
    "password": "+Password447",
    "password2": "+Password447",
    "scope": ["me"],
}


@pytest.fixture
async def create_user(client):
    await client.post("/users/create-user", json=default_user_data)


@pytest.fixture
async def token(client, create_user):
    auth = BearerAuth(app, user=default_user_data)
    yield await auth.async_get_token()
