from pydantic import BaseModel, Field


def create_ability(name, description, in_deth_description):
    return {
        "name": name,
        "description": description,
        "in_deth_description": in_deth_description,
    }

class Ability(BaseModel):
    name: str = Field(...)  # name of an ability 
    description: str = Field(...) # description of an ability
    in_deth_description: str = Field(...) # in_deth_description of an ability

    class Config:
        schema_extra = {
            "example": {"name": "Adaptability",
                        "description": "Powers up moves of the same type as the Pokémon.",
                        "in_deth_description": "Increases the Same Type Attack Bonus from *1.5 to *2.",
                        }
        }