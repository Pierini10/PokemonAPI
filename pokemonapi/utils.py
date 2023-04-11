from .models.pokemon import SearchPokemon
from .models.attack import SearchAttack


def possible_pokemon_searchs(query: SearchPokemon):
    searchParams = {"$and": [], "$or": []}

    if (name := query.name):
        name = prepareString(name)
        nameID = {"name": name}
        searchParams["$or"] = [
            {'$where': f'function() {{ for (var key in this.other_names) {{ if (this.other_names[key].indexOf("{name}") > -1) return true; }} return false; }}'}, nameID]

    if (query.national_number):
        searchParams["national_number"] = int(query.national_number)

    if (query.paldea_number):
        searchParams["paldea_number"] = int(query.paldea_number)

    if (types := query.type):
        for type in types:
            type = type.upper()
            searchParams["$and"].append(
                {'$where': f'function() {{ for (var key in this.type) {{ if (this.type[key].indexOf("{type}") > -1) return true; }} return false; }}'})
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
            weakness = weakness.upper()
            searchParams["$and"].append(
                {'$where': f'function() {{ for (var key in this.weakness) {{ if (this.weakness[key]["{weakness}"] > 1) return true; }} return false; }}'})

    if (resistance := query.resistance):
        for resist in resistance:
            resist = resist.upper()
            searchParams["$and"].append(
                {'$where': f'function() {{ for (var key in this.weakness) {{ if (this.weakness[key]["{resist}"] < 1) return true; }} return false; }}'})

    if (query.male):
        searchParams["gender.male"] = int(query.male)
    if (query.female):
        searchParams["gender.female"] = int(query.female)
    if (query.unknown):
        searchParams["gender.unknown"] = int(query.unknown)

    if (classification := query.classification):
        classification = prepareString(classification)
        searchParams["classification"] = {"$in": [classification]}

    if (query.hp):
        searchParams["stats.Stats.HP"] = int(query.hp)
    if (query.mthp):
        searchParams["$and"].append(
            prepare_stats_comp("HP", query.mthp, ">"))
    if (query.lthp):
        searchParams["$and"].append(
            prepare_stats_comp("HP", query.lthp, "<"))

    if (query.attack):
        searchParams["stats.Stats.Attack"] = int(query.attack)
    if (query.mtAttack):
        searchParams["$and"].append(
            prepare_stats_comp("Attack", query.mtAttack, ">"))
    if (query.ltAttack):
        searchParams["$and"].append(
            prepare_stats_comp("Attack", query.ltAttack, "<"))

    if (query.defense):
        searchParams["stats.Stats.Defense"] = int(query.defense)
    if (query.mtDefense):
        searchParams["$and"].append(
            prepare_stats_comp("Defense", query.mtdefense, ">"))
    if (query.ltDefense):
        searchParams["$and"].append(
            prepare_stats_comp("Defense", query.ltdefense, "<"))

    if (query.spAttack):
        searchParams["stats.Stats.Sp. Attack"] = int(query.spAttack)
    if (query.mtSpAttack):
        searchParams["$and"].append(
            prepare_stats_comp("Sp. Attack", query.mtSpAttack, ">"))
    if (query.ltSpAttack):
        searchParams["$and"].append(
            prepare_stats_comp("Sp. Attack", query.ltSpAttack, "<"))

    if (query.spDefense):
        searchParams["stats.Stats.Sp. Defense"] = int(query.spDefense)
    if (query.mtSpDefense):
        searchParams["$and"].append(
            prepare_stats_comp("Sp. Defense", query.mtSpDefense, ">"))
    if (query.ltSpDefense):
        searchParams["$and"].append(
            prepare_stats_comp("Sp. Defense", query.ltSpDefense, "<"))
        
    if (query.speed):
        searchParams["stats.Stats.Speed"] = int(query.speed)
    if (query.mtSpeed):
        searchParams["$and"].append(
            prepare_stats_comp("Speed", query.mtSpeed, ">"))
    if (query.ltSpeed):
        searchParams["$and"].append(
            prepare_stats_comp("Speed", query.ltSpeed, "<"))

    if (query.total):
        searchParams["stats.Stats.Total"] = int(query.total)
    if (query.mtTotal):
        searchParams["$and"].append(
            prepare_stats_comp("Total", query.mtTotal, ">"))
    if (query.ltTotal):
        searchParams["$and"].append(
            prepare_stats_comp("Total", query.ltTotal, "<"))

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
            findMove = {"$or": []}
            findMove["$or"].append({'moves.level_moves.Standard Level Up': {
                '$elemMatch': {'Attack Name': move}}})
            findMove["$or"].append({'moves.tm_moves.Normal': {
                '$elemMatch': {'Attack Name': move}}})
            findMove["$or"].append({'moves.egg_moves.Egg Moves': {
                '$in': [move]}})

            searchParams["$and"].append(findMove)

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


def prepare_stats_comp(key, value, comp: str):
    return {'$where': f'function() {{ for (const item of this.stats) {{for (key in item) {{  if (item[key]["{key}"] {comp} {int(value)}) return true; }}}} return false; }}'}
