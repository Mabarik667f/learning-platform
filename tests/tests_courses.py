import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from .helpers.test_class import BaseTestClass

# @pytest.mark.usefixtures("create_user", "create_course")
# class TestsForCourseApi(BaseTestClass):
#     prefix = '/courses'


#     async def test_struct_create(self, session: AsyncSession, token: str):
#         pass
