from fastapi import FastAPI, Request, Body, Response, APIRouter
from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient
from models import Pokemon
import json

app = FastAPI()
client = MongoClient("mongodb://127.0.0.1/")
db = client.get_database("pokemon")
collection = db.get_collection("pokemons")

router = APIRouter()


@app.post("/createPokemon", response_model=Pokemon)
def home(request: Request, pokemon: Pokemon = Body(...)):
    collection.insert_one(pokemon.dict())
    createdPokemon = collection.find_one({"name": pokemon.name})
    return createdPokemon


@app.get("/getPokemons", response_model=list[Pokemon])
def home(request: Request):
    pokemons = list(collection.find())
    print(pokemons)
    return pokemons
