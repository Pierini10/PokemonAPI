from pydantic import BaseModel, Field


class PokemonGender:
    MALE = "MALE"
    FEMALE = "FEMALE"
    UNKNOWN = "UNKNOWN"


class PokemonType:
    NORMAL = "NORMAL"
    FIRE = "FIRE"
    WATER = "WATER"
    ELECTRIC = "ELECTRIC"
    GRASS = "GRASS"
    ICE = "ICE"
    FIGHTING = "FIGHTING"
    POISON = "POISON"
    GROUND = "GROUND"
    FLYING = "FLYING"
    PSYCHIC = "PSYCHIC"
    BUG = "BUG"
    ROCK = "ROCK"
    GHOST = "GHOST"
    DRAGON = "DRAGON"
    DARK = "DARK"
    STEEL = "STEEL"
    FAIRY = "FAIRY"


class PokemonEgg(BaseModel):
    egg_steps: int = Field(...)
    egg_cycles: int = Field(...)
    egg_group: tuple = Field(...)  # (str, str)


class PokemonExperience(BaseModel):
    base_experience: int = Field(...)
    experience_growth: str = Field(...)


class PokemonAbility:
    name: str
    description: str
    is_hidden: bool


class PokemonEffortValue(BaseModel):
    value: int
    type: str


class PokemonWildHoldItem:
    name: str
    rarity: int
    image_link: str


class Pokemon(BaseModel):
    national_number: int = Field(...)  # id of pokemon
    paldea_number: int = Field(...)  # id of pokemon in paldea
    gender: dict = Field(...)  # {gender : probability}
    name: dict = Field(...)  # {language: name}
    image_link: dict = Field(...)  # {image_name: link}
    type: tuple = Field(...)
    classification: str = Field(...)
    height: dict = Field(...)  # {unit: height}
    weight: dict = Field(...)  # {unit: weight}
    capture_rate: int = Field(...)
    egg: PokemonEgg = Field(...)
    # (PokemonAbility, PokemonAbility, PokemonAbility)
    habilities: tuple = Field(...)
    experience: PokemonExperience = Field(...)
    base_happiness: int = Field(...)
    effort_values: PokemonEffortValue = Field(...)
    weakness: dict = Field(...)
    # (PokemonWildHoldItem, PokemonWildHoldItem, PokemonWildHoldItem)
    wild_hold_item: tuple = Field(...)

    class Config:
        schema_extra = {
            "example": {"national_number": 25,
                        "paldea_number": 1,
                        "gender": {"male": 25, "female": 75, "unknown": 0},
                        "name": {"en": "Pikachu", "es": "Pikachu", "jp": "ピカチュウ"},
                        "image_link": {"image_name": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png"},
                        "type": ("Electric", "Normal"),
                        "classification": "Mouse Pokémon",
                        "height": {"unit": "0.4 m"},
                        "weight": {"unit": "6.0 kg"},
                        "capture_rate": 190,
                        "egg": {"egg_steps": 5120, "egg_cycles": 20, "egg_group": ("Field", "Fairy")},
                        "habilities": ("Static", "Lightning Rod", "Static"),
                        "experience": {"base_experience": 112, "experience_growth": "Medium Fast"},
                        "base_happiness": 70,
                        "effort_values": {"value": 1, "type": "Speed"},
                        "weakness": {"Fire": 2, "Water": 2, "Electric": 0.5, "Grass": 0.5, "Ice": 2, "Fighting": 1, "Poison": 1},
                        "wild_hold_item": ("Potion", "Potion", "Potion")

                        }
        }
