from pydantic import BaseModel
from pydantic_core import CoreSchema, core_schema
from pydantic import GetCoreSchemaHandler
import re


def slugify(val: str) -> str:

    val = val.lower()
    val = re.sub(r"[\W_]+", '-', val)
    val = val.strip('-')
    return val


class Slug(str):

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: type, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        schema = handler(str)
        return core_schema.no_info_before_validator_function(slugify, schema)


class Category(BaseModel):
    title: str
    slug: Slug


class CreateCategory(Category):
    pass


class UpdateCategory(Category):
    pass


class CategoryResponse(Category):
    id: int

    class Config:
        from_attributes = True
