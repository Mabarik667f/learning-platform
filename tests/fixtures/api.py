import pytest
from httpx import AsyncClient

from loguru import logger


@pytest.fixture
async def create_categories(client: AsyncClient, token: dict):
    categories = ["Python", "Rust", "Algorithms"]
    for cat in categories:
        await client.post("/categories/create", json={"title": cat}, headers=token)


@pytest.fixture
async def create_course(client: AsyncClient, create_categories, token: dict):
    data = {
        "title": "string",
        "describe": "string",
        "img": "string",
        "price": 1,
        "difficulty": "easy",
        "categories": [1],
    }
    await client.post("/courses/create", json=data, headers=token)


@pytest.fixture
async def create_section(client: AsyncClient, create_course, token: dict):
    data = {
        "title": "Test section 1",
        "describe": "this section test 1",
        "course_id": 1,
        "position": 1,
        "subsections": [{"title": "Test subsection 1", "position": 1}],
    }
    await client.post("/sections/create", json=data, headers=token)


@pytest.fixture
async def create_subsection(client: AsyncClient, create_section, token: dict):
    data = {"title": "Test title 1", "section_id": 1, "position": 1}
    await client.post("/subsections/create", json=data, headers=token)
