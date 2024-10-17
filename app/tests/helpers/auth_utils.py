import httpx

from fastapi import FastAPI
from collections.abc import AsyncGenerator
from httpx import Request, Response, ASGITransport, AsyncClient
from loguru import logger


class BearerAuth(httpx.Auth):

    def __init__(self, app: FastAPI, user: dict, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.app = app
        self.user = user

    async def async_auth_flow(
        self, request: Request
    ) -> AsyncGenerator[Request, Response]:
        token = await self.async_get_token()
        request.headers["Authorization"] = f"Bearer {token}"
        yield request

    async def async_get_token(self) -> dict:
        async with AsyncClient(transport=ASGITransport(app=self.app), base_url="http://test") as client:  # type: ignore
            response = await client.post("/auth/token", data=self.user)
            token_data = response.json()
            return {"Authorization": f"Bearer {token_data.get("access_token")}"}
