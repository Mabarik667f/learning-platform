from pydantic import BaseModel

class Category(BaseModel):
    title: str

class CreateCategory(Category):
    pass


class UpdateCategory(Category):
    pass


class CategoryResponse(Category):
    id: int

    class Config:
        from_attributes = True
