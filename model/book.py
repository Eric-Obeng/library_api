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
    rating: float | None = Field(None, ge=0, le=5)

    @field_validator("title")
    @classmethod
    def capitalize_title(cls, v: str) -> str:
        return v.strip().title()

    @field_validator("author", "category", "description", mode="before")
    @classmethod
    def trim_whitespaces(cls, v: str) -> str:
        return v.strip()

    @field_validator("category", mode="before")
    @classmethod
    def _lower_category(cls, v):
        if isinstance(v, str):
            return v.lower()
        return v

    @field_validator("rating", mode="before")
    @classmethod
    def _validate_rating(cls, v):
        if v is None:
            return None
        try:
            val = float(v)
        except (TypeError, ValueError):
            raise ValueError("rating must be  a number between 0 and 5")
        if not (0 <= val <= 5):
            raise ValueError("rating must be  a number between 0 and 5")
        return val
