from httpx import AsyncClient
from loguru import logger
import pytest

# add create_course
@pytest.mark.usefixtures("create_user")
class TestForSections:

    prefix = "/sections/"

    @classmethod
    def get_endpoint(cls, url: str | int):
        return f"{cls.prefix}{url}"

    async def test_create_section(self, client: AsyncClient):
        # create course
        data = {"title": "Test section 1", "describe": "this section test 1", "course_id": 0}

        response = await client.get("/users/me")
        assert response.status_code == 200

    async def test_bulk_create_sections(self, client: AsyncClient):
        # create course
        data = {"title": "Test section 1", "describe": "this section test 1", "course_id": 0}
        response = await client.get("/users/me")
        assert response.status_code == 200

    async def test_patch_section(self, client: AsyncClient):
        response = await client.patch(self.get_endpoint("patch"))
        assert response.status_code == 200

    async def test_get_section(self, client: AsyncClient):
        response = await client.get(self.get_endpoint(0))

    async def test_get_list_sections(self, client: AsyncClient):
        response = await client.get(self.get_endpoint("list"))

    async def test_delete_section(self, client: AsyncClient):
        response = await client.delete(self.get_endpoint("delete"))
        assert response.status_code == 204
