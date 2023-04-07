from Models.pokemon import SearchPokemon

def possible_searches(query: SearchPokemon):
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


def prepareString(string: str):
    separation = string.split(" ")
    temp = []
    for item in separation:
        item = item[0].upper() + item[1:].lower()
        temp.append(item)
    return " ".join(temp)
