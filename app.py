from fastapi import FastAPI, Request, Body, Response, APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient
from models import Pokemon
import json

app = FastAPI()
client = MongoClient("mongodb://127.0.0.1/")
db = client.get_database("pokemon")
collection = db.get_collection("pokemons")

router = APIRouter()


def set_uniqueAttribute():
    collection.create_index("national_number", unique=True)
    collection.create_index("paldea_number", unique=True)
    collection.create_index("name", unique=True)


set_uniqueAttribute()


@app.post("/createPokemon")
def createPokemon(request: Request, pokemon: Pokemon = Body(...)):
    if collection.find_one({"national_number": pokemon.national_number, "paldea_number": pokemon.paldea_number,  "name":  pokemon.name}):
        raise HTTPException(status_code=400, detail="Pokemon already exists")
    collection.insert_one(pokemon.dict())
    createdPokemon = collection.find_one({"name": pokemon.name})
    return "Pokemon created successfully"


@app.get("/getPokemons", response_model=list[Pokemon])
def get(request: Request):
    pokemons = list(collection.find())
    print(pokemons)
    return pokemons


@app.delete("/deletePokemon/{national_number}")
def deletePokemon(request: Request, national_number: int):
    deleted = collection.delete_one(
        {"national_number": national_number}).deleted_count
    if (deleted == 0):
        raise HTTPException(status_code=404, detail="Pokemon not found")
    return {"message": "Pokemon deleted successfully"}
