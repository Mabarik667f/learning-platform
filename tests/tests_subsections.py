from httpx import AsyncClient
from loguru import logger
import pytest

@pytest.mark.usefixtures("create_user", "create_section")
class TestForSubsections:

    prefix = "/subsections/"

    @classmethod
    def get_endpoint(cls, url: str | int):
        return f"{cls.prefix}{url}"

    async def test_create_subsection(self, client: AsyncClient):
        data = {"title": "Test title 1", "section_id": 1}
        response = await client.post(self.get_endpoint("create"), json=data)
        assert response.status_code == 201
        assert response.json().get("title") == "Test title 1"

        data["section_id"] = 100
        response = await client.post(self.get_endpoint("create"), json=data)
        assert response.status_code == 400

    async def test_get_subsection(self, client: AsyncClient):
        subsection_id = 1
        response = await client.get(self.get_endpoint(subsection_id))
        assert response.status_code == 200
        assert response.json().get("section_id") == 1

        subsection_id = 100
        response = await client.get(self.get_endpoint(subsection_id))
        assert response.status_code == 400

    async def test_patch_subsection(self, client: AsyncClient):
        subsection_id = 1
        data = {"title": "New subsection title"}
        response = await client.patch(self.get_endpoint(f"patch/{subsection_id}"), json=data)
        assert response.status_code == 200
        assert response.json().get('title') == "New subsection title"

    async def test_list_subsection(self, client: AsyncClient):
        section_id = 1
        response = await client.get(self.get_endpoint(f"list/{section_id}"))
        assert response.status_code == 200
        assert len(response.json()) == 1

        section_id = 100
        response = await client.get(self.get_endpoint(f"list/{section_id}"))
        assert response.status_code == 400

    async def test_delete_subsection(self, client: AsyncClient):
        subsection_id = 1
        response = await client.delete(self.get_endpoint(f"delete/{subsection_id}"))
        assert response.status_code == 204
        response = await client.get(self.get_endpoint(subsection_id))
        logger.info(f"SUBSECTION = {response.json()}")
        assert response.status_code == 400

        subsection_id = 100
        response = await client.delete(self.get_endpoint(f"delete/{subsection_id}"))
        assert response.status_code == 400
