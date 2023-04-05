from pydantic import BaseModel, Field


class Pokemon(BaseModel):
    name: str = Field(...)
    type: str = Field(...)

    class Config:
        schema_extra = {
            "example": {"name": "Pikachu",
                        "type": "Electric"}
        }
