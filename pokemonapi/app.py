from fastapi import FastAPI, Request, Body, Response, APIRouter, HTTPException
from pymongo import MongoClient, TEXT
from pokemonapi.models.ability import Ability

from pokemonapi.webscrapping.ability import load_all_ability
from .utils import possible_searches
from .models.pokemon import Pokemon, SearchPokemon
from .models.attack import Attack
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
    createdPokemon = pokemon_collection.find_one({"name": pokemon.name})
    return "Pokemon created successfully"


@ app.post("/getPokemons", response_model=list[Pokemon])
def get(request: Request, pokemon: SearchPokemon = Body(None)):
    if (pokemon):
        searchParams = possible_searches(pokemon)
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


@ app.delete("/deletePokemon/{national_number}")
def deletePokemon(request: Request, national_number: int):

    deleted = pokemon_collection.delete_one(
        {"national_number": national_number}).deleted_count
    if (deleted == 0):
        raise HTTPException(status_code=404, detail="Pokemon not found")
    return {"message": "Pokemon deleted successfully"}

@ app.delete("/deletePokemon/{national_number}")
def deletePokemon(request: Request, national_number: int):

    deleted = pokemon_collection.delete_one(
        {"national_number": national_number}).deleted_count
    if (deleted == 0):
        raise HTTPException(status_code=404, detail="Pokemon not found")
    return {"message": "Pokemon deleted successfully"}

@ app.get("/loadAttacks")
def loadAttacks():
    attacks = load_all_attacks()
    for attack in attacks:
        if not attacks_collection.find_one({"name": attack["name"]}):
            attacks_collection.insert_one(attack)
        else:
            attacks_collection.update_one({"name": attack["name"]}, {"$set": attack})
    return {"message": "Attacks loaded successfully"}

@ app.get("/getAttacks", response_model=list[Attack])
def getAttacks():
    # TODO add search filters
    return list(attacks_collection.find())

@ app.get("/loadAbilities")
def loadAbilities():
    abilities = load_all_ability()
    for ability in abilities:
        if not abilities_collection.find_one({"name": ability["name"]}):
            abilities_collection.insert_one(ability)
        else:
            abilities_collection.update_one({"name": ability["name"]}, {"$set": ability})
    return {"message": "Abilities loaded successfully"}

@ app.get("/getAbilities", response_model=list[Ability])
def getAbilities():
    # TODO add search filters
    return list(abilities_collection.find())
