from httpx import AsyncClient
from loguru import logger
import pytest

# add create_section, create_course
@pytest.mark.usefixtures("create_user")
class TestForSubsections:

    prefix = "/subsections/"

    @classmethod
    def get_endpoint(cls, url: str | int):
        return f"{cls.prefix}{url}"

    async def test_create_subsection(self, client: AsyncClient):
        response = await client.post(self.get_endpoint("create"))
        assert response.status_code == 201

    async def test_get_subsection(self, client: AsyncClient):
        response = await client.get(self.get_endpoint(0))

    async def test_get_list_subsection(self, client: AsyncClient):
        response = await client.get(self.get_endpoint("list"))

    async def test_patch_subsection(self, client: AsyncClient):
        response = await client.get(self.get_endpoint("patch"))

    async def test_delete_subsection(self, client: AsyncClient):
        response = await client.get(self.get_endpoint("delete"))
        assert response.status_code == 204
