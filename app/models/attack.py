from pydantic import BaseModel, Field

class AttactCategory:
    PHYSICAL = "PHYSICAL"
    SPECIAL = "SPECIAL"
    OTHER = "OTHER"

class Attack(BaseModel):
    name: str = Field(...)  # name of an attack
    type: str = Field(...) # type of an attack
    category: str = Field(...) # category of an attack
    pp: int = Field(...) # pp of an attack
    damage: int = Field(...) # damage of an attack
    accuracy: int = Field(...) # accuracy of an attack
    effect: str = Field(...) # effect of an attack

    class Config:
        schema_extra = {
            "example": {"name": "Fire Punch",
                        "type": 1,
                        "category": AttactCategory.SPECIAL,
                        "pp": 15,
                        "damage": 75,
                        "accuracy": 100,
                        "effect": "The target is attacked with a fiery punch. This may also leave the target with a burn.",
                        }
        }
