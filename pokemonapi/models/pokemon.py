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
    egg_group: list = Field(...)  # (str, str)


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
    name: str = Field(...)  # {language: name}
    other_names: dict = Field(...)  # {language: name}
    image_link: dict = Field(...)  # {image_name: link}
    type: dict = Field(...)
    stats: list[dict] = Field(...)
    classification: str | list[str] = Field(...)
    height: dict = Field(...)  # {unit: height}
    weight: dict = Field(...)  # {unit: weight}
    capture_rate: int = Field(...)
    egg: PokemonEgg = Field(...)
    abilities: dict = Field(...)
    alternate_forms: list = Field(...)
    gender_differences: list = Field(...)
    # experience: PokemonExperience = Field(...)
    base_happiness: int = Field(...)
    effort_values: dict = Field(...)
    weakness: dict = Field(...)
    # (PokemonWildHoldItem, PokemonWildHoldItem, PokemonWildHoldItem)
    wild_hold_item: dict = Field(...)
    moves: dict = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "national_number": 25,
                "paldea_number": 74,
                "gender": {
                    "Male": 50,
                    "Female": 50
                },
                "name": "Pikachu",
                "other_names": {
                    "Japan": "Pikachu, ピカチュウ",
                    "French": "Pikachu",
                    "German": "Pikachu",
                    "Korean": "피카츄"
                },
                "image_link": {
                    "Normal Sprite": "https://www.serebii.net/scarletviolet/pokemon/new/025.png"
                },
                "type": {
                    "Normal": [
                        "ELECTRIC"
                    ]
                },
                "stats": [
                    {
                        "Stats": {
                            "HP": 35,
                            "Attack": 55,
                            "Defense": 40,
                            "Sp. Attack": 50,
                            "Sp. Defense": 50,
                            "Speed": 90,
                            "Total": 320
                        }
                    }
                ],
                "classification": "Mouse Pokémon",
                "height": {
                    "Normal Form": {
                        "feet": "1'04\"",
                        "m": 0.4
                    }
                },
                "weight": {
                    "Normal Form": {
                        "lbs": 13.2,
                        "kg": 6
                    }
                },
                "capture_rate": 190,
                "egg": {
                    "egg_steps": 1280,
                    "egg_cycles": 10,
                    "egg_group": [
                        "Field",
                        "Fairy"
                    ]
                },
                "abilities": {
                    "Normal Form": [
                        [
                            "Static",
                            False
                        ],
                        [
                            "Lightning Rod",
                            True
                        ]
                    ]
                },
                "alternate_forms": [
                    "Original Cap",
                ],
                "gender_differences": [
                    [
                        "Male Sprite",
                        "https://www.serebii.net/scarletviolet/pokemon/025.png"
                    ],
                    [
                        "Female Sprite",
                        "https://www.serebii.net/scarletviolet/pokemon/025-f.png"
                    ]
                ],
                "base_happiness": 50,
                "effort_values": {
                    "Normal Form": [
                        {
                            "type": "Speed",
                            "value": 2
                        }
                    ]
                },
                "weakness": {
                    "Normal Form": {
                        "NORMAL": 1
                    }
                },
                "wild_hold_item": {
                    "item": "Light Ball",
                    "percentage": 5
                },
                "moves": {
                    "level_moves": {
                        "Standard Level Up": [
                            {
                                "Level": "—",
                                "Attack Name": "Nuzzle"
                            }
                        ]
                    },
                    "tm_moves": {
                        "Normal": [
                            {
                                "TM": "TM001",
                                "Attack Name": "Take Down"
                            }

                        ]
                    },
                    "egg_moves": {
                        "Egg Moves": ["Flail"]
                    },
                    "reminder_moves": {},
                    "special_moves": {
                        "Special Moves": [
                            "Fly"
                        ]
                    },
                    "pre_evolve_moves": {}
                }
            }
        }


class EditablePokemon(BaseModel):
    national_number: int = Field(None)  # id of pokemon
    paldea_number: int = Field(None)  # id of pokemon in paldea
    gender: dict = Field(None)  # {gender : probability}
    name: dict = Field(None)  # {language: name}
    image_link: dict = Field(None)  # {image_name: link}
    type: tuple = Field(None)
    classification: str = Field(None)
    height: dict = Field(None)  # {unit: height}
    weight: dict = Field(None)  # {unit: weight}
    capture_rate: int = Field(None)
    egg: PokemonEgg = Field(None)
    # (PokemonAbility, PokemonAbility, PokemonAbility)
    abilities: dict = Field(None)
    experience: PokemonExperience = Field(None)
    base_happiness: int = Field(None)
    effort_values: PokemonEffortValue = Field(None)
    weakness: dict = Field(None)
    # (PokemonWildHoldItem, PokemonWildHoldItem, PokemonWildHoldItem)
    wild_hold_item: tuple = Field(None)
    alternate_forms: list = Field(None)

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
                        "abilities": {"Normal Form": [["Intimidate", False], ["Moxie", True]]},
                        "experience": {"base_experience": 112, "experience_growth": "Medium Fast"},
                        "base_happiness": 70,
                        "effort_values": {"value": 1, "type": "Speed"},
                        "weakness": {"Fire": 2, "Water": 2, "Electric": 0.5, "Grass": 0.5, "Ice": 2, "Fighting": 1, "Poison": 1},
                        "wild_hold_item": ("Potion", "Potion", "Potion"),
                        "alternate_forms": ["Original Cap"]
                        }
        }


class SearchPokemon(BaseModel):
    national_number: int = Field(None)  # id of pokemon
    paldea_number: int = Field(None)  # id of pokemon in paldea
    male: int = Field(None)  # {gender : probability}
    female: int = Field(None)
    unknown: int = Field(None)
    name: str = Field(None)  # {language: name}
    classification: str = Field(None)
    abilities: list = Field(None)
    type: list[str] = Field(None)
    weakness: list = Field(None)
    alternate_forms: list = Field(None)

    hp: int = Field(None)  # value of hp
    mthp: int = Field(None)  # more than hp
    lthp: int = Field(None)  # less than hp

    attack: int = Field(None)  # value of attack
    mtAttack: int = Field(None)  # more than attack
    ltAttack: int = Field(None)  # less than attack

    defense: int = Field(None)  # value of defense
    mtdefense: int = Field(None)  # more than defense
    ltdefense: int = Field(None)  # less than defense

    defense: int = Field(None)  # value of defense
    mtDefense: int = Field(None)  # more than defense
    ltDefense: int = Field(None)  # less than defense

    spAttack: int = Field(None)  # value of spattack
    mtSpAttack: int = Field(None)  # more than spattack
    ltSpAttack: int = Field(None)  # less than spattack

    spDefense: int = Field(None)  # value of spdefense
    mtSpDefense: int = Field(None)  # more than spdefense
    ltSpDefense: int = Field(None)  # less than spdefense

    speed: int = Field(None)  # value of speed
    mtSpeed: int = Field(None)  # more than speed
    ltSpeed: int = Field(None)  # less than speed

    total: int = Field(None)  # value of total
    mtTotal: int = Field(None)  # more than total
    ltTotal: int = Field(None)  # less than total

    captureRate: int = Field(None)  # value of capture_rate
    mtCaptureRate: int = Field(None)  # more than capture_rate
    ltCaptureRate: int = Field(None)  # less than capture_rate

    moves: list[str] = Field(None)
