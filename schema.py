
from pydantic import BaseModel, validator


class CreateAdv(BaseModel):
    title: str
    description: str
    owner: str

    @validator("title")
    def len_title(cls, value):
        if len(value) >= 30:
            raise ValueError("Оverlong title")
        return value
