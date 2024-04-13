from pydantic import BaseModel, Field


class CreateCategorySchema(BaseModel):
    name: str = Field(..., max_length=200)

    class ConfigDict:
        from_attributes = True


class UpdateCategorySchema(CreateCategorySchema):
    pass


class CategorySchema(BaseModel):
    id: int
    name: str
    slug: str
