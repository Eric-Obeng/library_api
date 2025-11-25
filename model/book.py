from pydantic import BaseModel, Field, field_validator


class Book(BaseModel):
    id: int
    title: str
    author: str
    category: str
    description: str | None = None
    rating: float | None = Field(None, min=0, max_digits=5)


class CreateBook(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=3)
    category: str = Field(...)
    description: str | None = Field(None)

    @field_validator("category", mode="before")
    def _lower_category(cls, v):
        if isinstance(v, str):
            return v.lower()
        return v
