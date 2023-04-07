from .models.pokemon import SearchPokemon
from .models.attack import SearchAttack


def possible_pokemon_searchs(query: SearchPokemon):
    searchParams = {"$and": []}
    if (name := query.name):
        name = name[0].upper() + name[1:].lower()
        en = {"name.en": name}
        es = {"name.es": name}
        jp = {"name.jp": name}
        searchParams["$or"] = [en, es, jp]

    if (query.national_number):
        searchParams["national_number"] = int(query.national_number)

    if (query.paldea_number):
        searchParams["paldea_number"] = int(query.paldea_number)

    if (type := query.type):
        type = type[0].upper() + type[1:].lower()
        searchParams["type"] = {
            "$in": [type]}

    if (habilities := query.habilities):
        temp = ""
        for item in habilities:
            temp = prepareString(item)
            searchParams["$and"].append({"habilities": {"$in": [temp]}})

    if (weaknesses := query.weakness):
        for weakness in weaknesses:
            weakness = weakness[0].upper() + weakness[1:].lower()
            searchParams['weakness.' + weakness] = {"$exists": True}

    if (query.male):
        searchParams["gender.male"] = int(query.male)
    if (query.female):
        searchParams["gender.female"] = int(query.female)
    if (query.unknown):
        searchParams["gender.unknown"] = int(query.unknown)

    if (classification := query.classification):
        classification = prepareString(classification)
        searchParams["classification"] = classification

    print(searchParams)
    if (searchParams["$and"] == []):
        del searchParams["$and"]
    return searchParams


def possible_attack_searchs(query: SearchAttack):
    searchParams = {"$and": []}
    if (name := query.name):
        name = prepareString(name)
        searchParams["name"] = name
    if (type := query.type):
        type = type.upper()
        searchParams["type"] = type
    if (category := query.category):
        category = category.upper()
        searchParams["category"] = category

    if (query.pp):
        searchParams["pp"] = int(query.pp)
    if (query.mtPp):
        searchParams["$and"].append({"pp": {"$gte": int(query.mtPp)}})
    if (query.ltPp):
        searchParams["$and"].append({"pp": {"$lte": int(query.ltPp)}})

    if (query.damage):
        searchParams["damage"] = int(query.damage)
    if (query.mtDamage):
        searchParams["$and"].append({"damage": {"$gte": int(query.mtDamage)}})
    if (query.ltDamage):
        searchParams["$and"].append({"damage": {"$lte": int(query.ltDamage)}})

    if (query.accuracy):
        searchParams["accuracy"] = int(query.accuracy)
    if (query.mtAccuracy):
        searchParams["$and"].append(
            {"accuracy": {"$gte": int(query.mtAccuracy)}})
    if (query.ltAccuracy):
        searchParams["$and"].append(
            {"accuracy": {"$lte": int(query.ltAccuracy)}})

    print(searchParams)
    if (searchParams["$and"] == []):
        del searchParams["$and"]
    return searchParams


def prepareString(string: str):
    separation = string.split(" ")
    temp = []
    for item in separation:
        item = item[0].upper() + item[1:].lower()
        temp.append(item)
    return " ".join(temp)
