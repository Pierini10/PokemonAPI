

def possible_Queries(query: dict):
    searchParams = {}
    if (name := query.get("name")):
        name = name[0].upper() + name[1:].lower()
        en = {"name.en": name}
        es = {"name.es": name}
        jp = {"name.jp": name}
        searchParams["$or"] = [en, es, jp]

    if (query.get("national_number")):
        searchParams["national_number"] = int(query.get("national_number"))

    if (query.get("paldea_number")):
        searchParams["paldea_number"] = int(query.get("paldea_number"))

    if (type := query.get("type")):
        type = type[0].upper() + type[1:].lower()
        searchParams["type"] = {
            "$in": [type]}

    if (habilities := query.get("habilities")):
        habilities = habilities[0].upper() + habilities[1:].lower()
        searchParams["habilities"] = {"$in": [habilities]}

    if (query.get("male")):
        searchParams["gender.male"] = int(query.get("male"))
    if (query.get("female")):
        searchParams["gender.female"] = int(query.get("female"))
    if (query.get("unknown")):
        searchParams["gender.unknown"] = int(query.get("unknown"))

    if (classification := query.get("classification")):
        separation = classification.split(" ")
        temp = []
        for item in separation:
            item = item[0].upper() + item[1:].lower()
            temp.append(item)
        classification = " ".join(temp)
        searchParams["classification"] = classification

    return searchParams
