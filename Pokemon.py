
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

class PokemonEgg:
    egg_steps: int
    egg_cycles: int
    egg_group: tuple # (str, str)

class PokemonExperience:
    base_experience: int
    experience_growth: str

class PokemonAbility:
    name: str
    description: str
    is_hidden: bool

class PokemonEffortValue:
    value: int
    type: str

class PokemonWildHoldItem:
    name: str
    rarity: int
    image_link: str

class Pokemon:
    national_number: int # id of pokemon
    paldea_number: int
    gender: dict # {gender : probability}
    name: dict # {language: name}
    image_link: dict # {image_name: link}
    type: tuple
    classification: str
    height: dict # {unit: height}
    weight: dict # {unit: weight}
    capture_rate: int
    egg: PokemonEgg
    habilities: tuple # (PokemonAbility, PokemonAbility, PokemonAbility)
    experience: PokemonExperience
    base_happiness: int
    effort_values: PokemonEffortValue
    weakness: dict
    wild_hold_item: tuple # (PokemonWildHoldItem, PokemonWildHoldItem, PokemonWildHoldItem)


    def callculate_weakness(self):
        pass

