from .models.pokemon import SearchPokemon
from .models.attack import SearchAttack


def possible_pokemon_searchs(query: SearchPokemon):
    searchParams = {"$and": [], "$or": []}

    if (name := query.name):
        name = name[0].upper() + name[1:].lower()
        nameID = {"name": name}
        jp = {"other_names.Japan": name}
        fr = {"other_names.French": name}
        gr = {"other_names.German": name}
        kr = {"other_names.Korean": name}
        searchParams["$or"] = [jp, fr, gr, kr, nameID]

    if (query.national_number):
        searchParams["national_number"] = int(query.national_number)

    if (query.paldea_number):
        searchParams["paldea_number"] = int(query.paldea_number)

    if (types := query.type):
        for type in types:
            type = type.upper()
            searchParams["$and"].append({"type.Normal": {
                "$in": [type]}})
    if (alternate_forms := query.alternate_forms):
        for form in alternate_forms:
            form = prepareString(form)
            searchParams["$and"].append({"alternate_forms": {"$in": [form]}})

    if (abilities := query.abilities):
        temp = ""
        for item in abilities:
            temp = prepareString(item)
            searchParams["$and"].append(
                {"abilities.Normal Form": {"$elemMatch": {"$elemMatch": {"$in": [temp]}}}})

    if (weaknesses := query.weakness):
        for weakness in weaknesses:
            weakness = weakness[0].upper() + weakness[1:].lower()
            searchParams['weakness["Normal Form"].' +
                         weakness] = {"$exists": True}

    if (query.male):
        searchParams["gender.male"] = int(query.male)
    if (query.female):
        searchParams["gender.female"] = int(query.female)
    if (query.unknown):
        searchParams["gender.unknown"] = int(query.unknown)

    if (classification := query.classification):
        classification = prepareString(classification)
        searchParams["classification"] = classification

    if (query.hp):
        searchParams["stats.Stats.HP"] = int(query.hp)
    if (query.mthp):
        searchParams["$and"].append(
            {"stats.Stats.HP": {"$gte": int(query.mtHp)}})
    if (query.lthp):
        searchParams["$and"].append(
            {"stats.Stats.HP": {"$lte": int(query.ltHp)}})

    if (query.attack):
        searchParams["stats.Stats.Attack"] = int(query.attack)
    if (query.mtAttack):
        searchParams["$and"].append(
            {"stats.Stats.Attack": {"$gte": int(query.mtAttack)}})
    if (query.ltAttack):
        searchParams["$and"].append(
            {"stats.Stats.Attack": {"$lte": int(query.ltAttack)}})

    if (query.defense):
        searchParams["stats.Stats.Defense"] = int(query.defense)
    if (query.mtDefense):
        searchParams["$and"].append(
            {"stats.Stats.Defense": {"$gte": int(query.mtDefense)}})
    if (query.ltDefense):
        searchParams["$and"].append(
            {"stats.Stats.Defense": {"$lte": int(query.ltDefense)}})

    if (query.spAttack):
        searchParams["stats.Stats.Sp. Attack"] = int(query.spAttack)
    if (query.mtSpAttack):
        searchParams["$and"].append(
            {"stats.Stats.Sp. Attack": {"$gte": int(query.mtSpAttack)}})
    if (query.ltSpAttack):
        searchParams["$and"].append(
            {"stats.Stats.Sp. Attack": {"$lte": int(query.ltSpAttack)}})

    if (query.spDefense):
        searchParams["stats.Stats.Sp. Defense"] = int(query.spDefense)
    if (query.mtSpDefense):
        searchParams["$and"].append(
            {"stats.Stats.Sp. Defense": {"$gte": int(query.mtSpDefense)}})
    if (query.ltSpDefense):
        searchParams["$and"].append(
            {"stats.Stats.Sp. Defense": {"$lte": int(query.ltSpDefense)}})

    if (query.speed):
        searchParams["stats.Stats.Speed"] = int(query.speed)
    if (query.mtSpeed):
        searchParams["$and"].append(
            {"stats.Stats.Speed": {"$gte": int(query.mtSpeed)}})
    if (query.ltSpeed):
        searchParams["$and"].append(
            {"stats.Stats.Speed": {"$lte": int(query.ltSpeed)}})

    if (query.total):
        searchParams["stats.Stats.Total"] = int(query.total)
    if (query.mtTotal):
        searchParams["$and"].append(
            {"stats.Stats.Total": {"$gte": int(query.mtTotal)}})
    if (query.ltTotal):
        searchParams["$and"].append(
            {"stats.Stats.Total": {"$lte": int(query.ltTotal)}})

    if (query.captureRate):
        searchParams["capture_rate"] = int(query.captureRate)
    if (query.mtCaptureRate):
        searchParams["$and"].append(
            {"capture_rate": {"$gte": int(query.mtCaptureRate)}})
    if (query.ltCaptureRate):
        searchParams["$and"].append(
            {"capture_rate": {"$lte": int(query.ltCaptureRate)}})

    if (moves := query.moves):
        for move in moves:
            move = prepareString(move)
            searchParams["$or"].append({'moves.level_moves.Standard Level Up': {
                                       '$elemMatch': {'Attack Name': move}}})
            searchParams["$or"].append({'moves.tm_moves.Normal': {
                                       '$elemMatch': {'Attack Name': move}}})
            searchParams["$or"].append({'moves.egg_moves.Egg Moves': {
                                       '$in': [move]}})

    if (searchParams["$and"] == []):
        del searchParams["$and"]
    if (searchParams["$or"] == []):
        del searchParams["$or"]
    print(searchParams)
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
