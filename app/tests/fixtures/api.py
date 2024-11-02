import json
import pytest
from httpx import AsyncClient

from loguru import logger

from tests.helpers.dummy_files import (
    create_dummy_txt,
    create_dummy_img,
    create_dummy_video,
)


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
        "price": 1,
        "difficulty": "easy",
        "categories": [1],
    }
    img = create_dummy_img()

    await client.post("/courses/create", files={"img": img}, data=data, headers=token)


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


@pytest.fixture
async def create_task(client: AsyncClient, create_subsection, token: dict):

    data = {
        "task_type": "test",
        "text": "This text for test-task 2",
        "subsection_id": 1,
    }

    video = create_dummy_video()
    task_tests = [
        ("task_tests", (f"dummy{i}.txt", create_dummy_txt(f"dummy{i}")))
        for i in range(2)
    ]
    files = [("video", ("video.mp4", video))] + task_tests

    await client.post("/tasks/create", files=files, data=data, headers=token)


@pytest.fixture
async def create_answers_for_task(client: AsyncClient, create_task, token: dict):
    answers = [
        {"text": "first", "is_correct": False},
        {"text": "second", "is_correct": True},
    ]

    await client.post("/tasks/add-answers/1", json=answers, headers=token)
