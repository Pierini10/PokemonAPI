from fastapi import FastAPI, Request, Body, Response, APIRouter, HTTPException
from pymongo import MongoClient, TEXT
from .models.ability import Ability
from .models.pokemon import Pokemon, SearchPokemon, EditablePokemon
from .models.attack import Attack, SearchAttack, EditableAttack

from .utils import possible_pokemon_searchs, possible_attack_searchs, prepareString
from .webscrapping.ability import load_all_ability
from .webscrapping.attack import load_all_attacks

app = FastAPI()
client = MongoClient("mongodb://127.0.0.1/")
db = client.get_database("pokemon")
pokemon_collection = db.get_collection("pokemons")
attacks_collection = db.get_collection("attacks")
abilities_collection = db.get_collection("abilities")
router = APIRouter()


def set_uniqueAttributes():
    pokemon_collection.create_index("national_number", unique=True)
    pokemon_collection.create_index("paldea_number", unique=True)
    pokemon_collection.create_index("name", unique=True)
    attacks_collection.create_index("name", unique=True)
    abilities_collection.create_index("name", unique=True)


set_uniqueAttributes()


@ app.post("/createPokemon")
def createPokemon(request: Request, pokemon: Pokemon = Body(...)):
    if pokemon_collection.find_one({"national_number": pokemon.national_number, "paldea_number": pokemon.paldea_number,  "name":  pokemon.name}):
        raise HTTPException(status_code=400, detail="Pokemon already exists")
    pokemon_collection.insert_one(pokemon.dict())
    return "Pokemon created successfully"


@ app.post("/createAttack")
def createAttack(request: Request, attack: Attack = Body(...)):
    if (attacks_collection.find_one({"name": attack.name})):
        raise HTTPException(status_code=400, detail="Attack already exists")
    attacks_collection.insert_one(attack.dict())
    return "Attack created successfully"


@ app.post("/createAbility")
def createAbility(request: Request, ability: Ability = Body(...)):
    if (abilities_collection.find_one({"name": ability.name})):
        raise HTTPException(status_code=400, detail="Ability already exists")
    abilities_collection.insert_one(ability.dict())
    return "Ability created successfully"


@ app.post("/getPokemons", response_model=list[Pokemon])
def get(request: Request, pokemon: SearchPokemon = Body(None)):
    if (pokemon):
        searchParams = possible_pokemon_searchs(pokemon)
        if (searchParams):
            pokemons = list(pokemon_collection.find(searchParams))
            if (len(pokemons) == 0):
                raise HTTPException(
                    status_code=404, detail="Pokemon not found")
        else:
            raise HTTPException(status_code=400, detail="Invalid search")
    else:
        pokemons = list(pokemon_collection.find())
    return pokemons


@ app.post("/getAttacks", response_model=list[Attack])
def getAttacks(request: Request, attack: SearchAttack = Body(None)):
    if (attack):
        searchParams = possible_attack_searchs(attack)
        if (searchParams):
            attacks = list(attacks_collection.find(searchParams))
            if (len(attacks) == 0):
                raise HTTPException(
                    status_code=404, detail="Attack not found")
        else:
            raise HTTPException(status_code=400, detail="Invalid search")

    else:
        attacks = list(attacks_collection.find())
    return attacks


@ app.get("/getAbilities/{name}", response_model=list[Ability])
def getAbilities(request: Request, ability: str | None = None):
    if (ability):
        ability = prepareString(ability)
        return list(abilities_collection.find({"name": ability}))
    print("getAbilities")
    return list(abilities_collection.find())


@app.put("/updatePokemon/{national_number}")
def updatePokemon(request: Request, national_number: int, pokemon: EditablePokemon = Body(...)):
    pokemon = pokemon.dict()
    filtered = {k: v for k, v in pokemon.items() if v is not None}
    pokemon.update(filtered)
    if (pokemon_collection.find_one({"national_number": national_number})):
        pokemon_collection.update_one(
            {"national_number": national_number}, {"$set": pokemon})
        return {"message": "Pokemon updated successfully"}
    raise HTTPException(status_code=404, detail="Pokemon not found")


@app.put("/updateAttack/{name}")
def updateAttack(request: Request, attack: EditableAttack):
    attack = attack.dict()
    filtered = {k: v for k, v in attack.items() if v is not None}
    attack.update(filtered)
    if (attacks_collection.find_one({"name": attack["name"]})):
        attacks_collection.update_one(
            {"name": attack["name"]}, {"$set": attack})
        return {"message": "Attack updated successfully"}
    raise HTTPException(status_code=404, detail="Attack not found")


@app.put("/updateAbility/{name}")
def updateAbility(request: Request, ability: Ability):
    ability = ability.dict()
    filtered = {k: v for k, v in ability.items() if v is not None}
    ability.update(filtered)
    if (abilities_collection.find_one({"name": ability["name"]})):
        abilities_collection.update_one(
            {"name": ability["name"]}, {"$set": ability})
        return {"message": "Ability updated successfully"}
    raise HTTPException(status_code=404, detail="Ability not found")


@ app.delete("/deletePokemon/{national_number}")
def deletePokemon(request: Request, national_number: int):

    deleted = pokemon_collection.delete_one(
        {"national_number": national_number}).deleted_count
    if (deleted == 0):
        raise HTTPException(status_code=404, detail="Pokemon not found")
    return {"message": "Pokemon deleted successfully"}


@ app.delete("/deleteAttack/{name}")
def deleteAttack(request: Request, name: str):
    name = prepareString(name)
    deleted = attacks_collection.delete_one({"name": name}).deleted_count
    if (deleted == 0):
        raise HTTPException(status_code=404, detail="Attack not found")
    return {"message": "Attack deleted successfully"}


@ app.delete("/deleteAbility/{name}")
def deleteAbility(request: Request, name: str):
    name = prepareString(name)
    deleted = abilities_collection.delete_one({"name": name}).deleted_count
    if (deleted == 0):
        raise HTTPException(status_code=404, detail="Ability not found")
    return {"message": "Ability deleted successfully"}


@ app.get("/loadPokemons")
def loadPokemons():
    pokemons = loadPokemons()
    for pokemon in pokemons:
        if not pokemon_collection.find_one({"national_number": pokemon['national_number']}):
            pokemon_collection.insert_one(pokemon)
        else:
            pokemon_collection.update_one(
                {"national_number": pokemon['national_number']}, {"$set": pokemon})
    return {"message": "Pokemons loaded successfully"}


@ app.get("/loadAttacks")
def loadAttacks():
    attacks = load_all_attacks()
    for attack in attacks:
        if not attacks_collection.find_one({"name": attack["name"]}):
            attacks_collection.insert_one(attack)
        else:
            attacks_collection.update_one(
                {"name": attack["name"]}, {"$set": attack})
    return {"message": "Attacks loaded successfully"}


@ app.get("/loadAbilities")
def loadAbilities():
    abilities = load_all_ability()
    for ability in abilities:
        if not abilities_collection.find_one({"name": ability["name"]}):
            abilities_collection.insert_one(ability)
        else:
            abilities_collection.update_one(
                {"name": ability["name"]}, {"$set": ability})
    return {"message": "Abilities loaded successfully"}
