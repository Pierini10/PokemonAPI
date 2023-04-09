from bs4 import BeautifulSoup
import re
from .utils import get_html_from_url, base_url


def get_all_types_pages(main_page):
    soup = BeautifulSoup(main_page, 'html.parser')
    type_group = soup.select_one("p:-soup-contains('By Type')").find("div").find_all("td")
    types_pages = []
    for type_line in type_group:
         types_pages.extend([f"{base_url}{t['href']}" for t in type_line.find_all("a")])
    return types_pages

def get_all_pokemon_from_page(page):
    soup = BeautifulSoup(page, 'html.parser')
    pokemons_entrys = soup.select_one("p:-soup-contains('The Pokémon below are the Pokémon of the')").find_all("table")

    return [f"{base_url}{pokemon_entry.find('a')['href']}" for pokemon_entry in pokemons_entrys[1:]]


def get_poke_pictures(data):
    pictures = {}
    
    for img in data.find_all("img"):
        if img.get("alt"):
            pictures[img.get("alt")] = f"{base_url}{img.get('src')}"
        else:
            pictures["Shiny Sprite"] = f"{base_url}{img.get('src')}"
            
    
    return pictures

def get_poke_info(data:BeautifulSoup):
    info = {}
    rows = data.find_all('tr', recursive=False)
    for i in range(2):
        headers = rows[0 + 2 * i].find_all('td', recursive=False)
        values = rows[1 + 2 * i].find_all('td', recursive=False)
    
        for i in range(len(headers)):
            value = values[i]
            attrib = headers[i]
            if table := value.find("table"):
                dic = {}
                trows = table.find_all('tr', recursive=False)
                
                for row in trows:
                    pairs = row.find_all('td', recursive=False)
                    
                    if b := pairs[0].find('b'):
                        key = b.text.split(' ')[0]
                    else:
                        key = pairs[0].text.split(' ')[0]
                        
                    if imgs := pairs[1].find_all("img"):
                        val = [img.get('alt').split('-')[0].upper() for img in imgs]
                    else:
                        if pairs[1].find('br'):
                            val = pairs[1].get_text(separator=', ')
                        else:
                            val = pairs[1].text
                    
                    dic[key] = val
                
                info[attrib.text] = dic
                
            elif imgs := value.find_all("img"):
                info[attrib.text] = [img.get('alt').split('-')[0].upper() for img in imgs]
                
            else:
                br_tags = value.find_all('br')
                if len(br_tags) > 0:
                    valList = []
                    valList.append(br_tags[0].previousSibling.strip())
                    for br_tag in br_tags:
                        valList.append(br_tag.nextSibling.strip())
                        
                    #ver passagens para unidades
                    
                    info[attrib.text] = valList
                else:
                    info[attrib.text] = value.text
 
    return info

def get_poke_more_info(data:BeautifulSoup):
    info = {}
    rows = data.find_all('tr', recursive=False)
    
    hasForms = False
    formsAbilities = {}
    tags = []
    
    for tag in rows[0].find('td').children:
        if tag.name == 'a' or tag.name == 'i':
            tags.append(tag)
        elif 'Form' in tag:
            hasForms = True
            formsAbilities[tag.split()[0].split('(')[1] + ' Form'] = tags
            tags = []
        elif 'Male' in tag or 'Female' in tag:
            hasForms = True
            formsAbilities[tag.split('(')[1].split(')')[0]] = tags
            tags = []
    
    if not hasForms:
        formsAbilities['Normal Form'] = tags
        
    for form in formsAbilities:
        abilities = []
        for i in range(len(formsAbilities[form])):
            tag = formsAbilities[form][i]
            if tag.name == 'a':
                hidden = False
                
                if i + 1 < len(formsAbilities[form]) and formsAbilities[form][i + 1].name == 'i':
                    hidden = True
                
                abilities.append((tag.text, hidden))
        
        formsAbilities[form] = abilities   
                
    info['Abilities'] = formsAbilities
    
    headers = rows[2].find_all('td', recursive=False)
    values = rows[3].find_all('td', recursive=False)
    
    for i in range(len(headers)):
        if headers[i].text.strip() != '':
            br_tags = values[i].find_all('br')
            if len(br_tags) > 0:
                valList = []
                
                for br_tag in br_tags:
                    
                    if(br_tag.previousSibling):
                        if br_tag.previousSibling.name == 'b':
                            valList.append(br_tag.previousSibling.text.strip())
                        else:
                            valList.append(br_tag.previousSibling.strip())
                    
                info[headers[i].text] = valList
            else:
                info[headers[i].text] = values[i].text

    return info

def get_poke_weakness(data:BeautifulSoup):
    info = {}
    
    rows = data.find_all('tr', recursive=False)
    headers = rows[1].find_all('td')
    
    for i in range(1, len(rows), 2):
        title = rows[i].find('i')
        values = rows[i + 1].find_all('td')
        
        weakness = {}

        for i in range(len(headers)):
            val = float(values[i].text.split('*')[1])
            weakness[headers[i].find('a')['href'].split('/')[-1].split('.')[0].upper()] = val
            
        if title:   
            info[title.text] = weakness
        else:
            info['Normal Form'] = weakness
    
    return info

def get_poke_even_more_info(data:BeautifulSoup):
    info = {}
    rows = data.find_all('tr', recursive=False)
    headers = rows[0].find_all('td', recursive=False)
    values = rows[1].find_all('td', recursive=False)
    
    egg_groups = values[1].find_all('a')
    
    for i in range(len(egg_groups)):
        egg_groups[i] = egg_groups[i].text
    
    info[headers[0].text] = values[0].text.strip()
    info[headers[1].text] = egg_groups
    
    return info

def get_evolution_chain(data:BeautifulSoup):
    info = {}
    name = data.find('td', class_="fooevo")
    table = data.find('table', class_="evochain")
    rows = table.find_all('tr', recursive=False)
    
    for row in rows:
        chain = row.find_all('img')
        
        for i in range(len(chain)):
            print(chain[i])
            if i % 2 == 0:
                if chain[i].has_attr('alt'):
                    chain[i] = chain[i]['alt']
                else:
                    chain[i] = chain[i].parent['href'].split('/')[-1].capitalize()
                    
            else:
                print('aqui')
                if chain[i].has_attr('alt'):
                    alt = chain[i]['alt']
                else:
                    alt = chain[i]['title']
                    
                if alt == 'Level ':
                    alt += chain[i]['src'].split('/')[-1].split('.')[0].split('l')[1]
                    
                chain[i] = alt
            
    
        info.setdefault(name.text, []).append(chain)
    
    return info

def get_poke_gender_differences(data:BeautifulSoup):
    info = []
    hasDifferences = data.find("td", string="Gender Differences")
    
    if hasDifferences:
        formsTable = data.find("table")
        rows = formsTable.find_all('tr', recursive=False)
        
        imgs = rows[1].find_all('img')
        
        for img in imgs:
            info.append((img['alt'], base_url + img['src']))
        
        return True, info
    else:
        return False, info

def get_poke_alternate_forms(data:BeautifulSoup):
    info = []
    hasForms = data.find("td", string="Alternate Forms")
    
    if hasForms:
        formsTable = data.find("table")
        rows = formsTable.find_all('tr', recursive=False)
        for row in rows[::3]:
            forms = row.find_all('td')
            for form in forms:
                info.append(form.text)
            
        return True, info
    else:
        return False, info
    
def get_poke_level_moves(data:BeautifulSoup):
    info = {}
    title = data.find(lambda tag: tag.name == "h3" and "Level Up" in tag.text)
    
    if title:
        rows = data.find_all('tr', recursive=False)
        moves = []
        
        for move in rows[2::2]:
            m = {}
            fields = move.find_all('td', recursive=False)

            m['Level'] = fields[0].text
            m['Attack Name'] = fields[1].find('a').text
            
            moves.append(m)
            
        info[title.text] = moves
        
        return True, info
    else:
        return False, info

def get_poke_tm_moves(data:BeautifulSoup):
    info = {}
    hasMoves = data.find("h3", string="Technical Machine Attacks")
    
    if hasMoves:
        rows = data.find_all('tr', recursive=False)
        hasForms = False
        
        if len(rows[2].find_all('td', recursive=False)) == 9:
            hasForms = True
        
        for move in rows[2::2]:
            m = {}
            fields = move.find_all('td', recursive=False)
            
            m['TM'] = fields[0].text
            m['Attack Name'] = fields[1].find('a').text
            
            if hasForms:
                for img in fields[-1].find_all('img'):
                    info.setdefault(img['alt'], []).append(m)
            else:
                info.setdefault("Normal", []).append(m)
            
        return True, info
    else:
        return False, info

def get_poke_egg_moves(data:BeautifulSoup):
    info = {}
    hasEgg = data.find("h3", string="Egg Moves")
    
    if hasEgg:
        rows = data.find_all('tr', recursive=False)
        moves = []
        
        for move in rows[2::2]:
            fields = move.find_all('td', recursive=False)
            
            moves.append(fields[0].find('a').text)
            
        info['Egg Moves'] = moves
        
        return True, info
    else:
        return False, info

def get_poke_reminder_moves(data:BeautifulSoup):
    info = {}
    hasMoves = data.find("h3", string="Move Reminder Only Attacks")
    hasMoves2 = data.find("h3", string="Move Reminder Exclusive Attacks")
    
    if hasMoves or hasMoves2:
        rows = data.find('thead').find_all('tr', recursive=False)
        moves = []
        
        for move in rows[2::2]:
            fields = move.find_all('td', recursive=False)
            
            moves.append(fields[0].find('a').text)
            
        info['Reminder Moves'] = moves
        
        return True, info
    else:
        return False, info

def get_poke_pre_evo_moves(data:BeautifulSoup):
    info = {}
    hasPreEvo = data.find("td", string="Pre-Evolution Only Moves")
    
    if hasPreEvo:
        rows = data.find_all('tr', recursive=False)
        moves = []
        
        for move in rows[2::2]:
            m = {}
            fields = move.find_all('td', recursive=False)
            
            method = fields[-1].find_all('td')
            
            m['Attack Name'] = fields[0].text
            m['Method'] = (method[0].find('img')['alt'], method[1].text)
        
            moves.append(m)
        
        info['Pre-Evolution Only Moves'] = moves
        
        return True, info
    else:
        return False, info
    
def get_poke_special_moves(data:BeautifulSoup):
    info = {}
    hasMoves = data.find("td", string="Special Moves")
    
    if hasMoves:
        rows = data.find('thead').find_all('tr', recursive=False)
        moves = []
        
        for move in rows[2::2]:
            fields = move.find_all('td', recursive=False)
            
            moves.append(fields[0].text)
        
        info['Special Moves'] = moves
        
        return True, info
    else:
        return False, info

def get_poke_stats(data:BeautifulSoup):
    info = {}
    rows = data.find_all('tr', recursive=False)
    
    headers = rows[1].find_all('td', recursive=False)
    values = rows[2].find_all('td', recursive=False)
    stats = {}
    total = 0
    
    for i in range(1, len(headers)):
        stat = int(values[i].text) 
        total += stat
        stats[headers[i].text] = stat
    
    stats['Total'] = total
    info[rows[0].find('h2').text] = stats
    
    return info

def join_data(pictures, info, more_info, even_more_info, weakness, gender_differences, alternate_forms, moves, stats):
    pokemon = {}
    
    pokemon['abilities'] = more_info['Abilities']
    pokemon['alternate_forms'] = alternate_forms
    pokemon['base_happiness'] = int(more_info['Base Happiness'])
    pokemon['capture_rate'] = int(info['Capture Rate'])
    pokemon['classification'] = info['Classification']
    pokemon['gender_differences'] = gender_differences
    pokemon['image_link'] = pictures
    pokemon['paldea_number'] = int(info['No.']['Paldea'].split('#')[1])
    pokemon['moves'] = moves
    pokemon['name'] = info['Name']
    pokemon['national_number'] = int(info['No.']['National'].split('#')[1])
    pokemon['other_names'] = info['Other Names']
    pokemon['stats'] = stats
    pokemon['type'] = info['Type']
    pokemon['weakness'] = weakness
    
    gender = {}
    if isinstance(info['Gender Ratio'], str):
        gender['Unknown'] = 100
    else:
        for g in info['Gender Ratio']:
            gender[g] = int(info['Gender Ratio'][g].split('%')[0].split('*')[0])
            
    pokemon['gender'] = gender
    
    height = {}
    form = 'Normal Form'
    
    for h in info['Height']:
        split_height = h.split(' / ')
        if len(split_height) > 1:
            for i in range(len(split_height)):
                if alternate_forms[i] not in height:
                    height[alternate_forms[i]] = {}
                
                if "'" in split_height[i]:
                    height[alternate_forms[i]]['feet'] = split_height[i]
                else:
                    match = re.match(r"(\d+(?:\.\d+)?)\D", split_height[i])
                    value = match.group(1)
                    unit = split_height[i][len(value):] 
                    height[alternate_forms[i]][unit] = float(value)
        else:
            if form not in height:
                height[form] = {}
            
            if "'" in h:
                height[form]['feet'] = h
            else:
                match = re.match(r"(\d+(?:\.\d+)?)\D", h)
                value = match.group(1)
                unit = h[len(value):] 
                height[form][unit] = float(value)
    
    pokemon['height'] = height
    
    weight = {}
    
    for w in info['Weight']:
        split_weight = w.split(' / ')
        if len(split_weight) > 1:
            for i in range(len(split_weight)):
                if alternate_forms[i] not in weight:
                    weight[alternate_forms[i]] = {}
                
                match = re.match(r"(\d+(?:\.\d+)?)\D", split_weight[i])
                value = match.group(1)
                unit = split_weight[i][len(value):] 
                weight[alternate_forms[i]][unit] = float(value)
        else:
            if form not in weight:
                weight[form] = {}
            
            match = re.match(r"(\d+(?:\.\d+)?)\D", w)
            value = match.group(1)
            unit = w[len(value):] 
            weight[form][unit] = float(value)
    
    pokemon['weight'] = weight
    
    egg = {}
    egg['egg_steps'] = int(info['Base Egg Steps'][0].split()[0].replace(',', ''))
    egg['egg_cycles'] = int(info['Base Egg Steps'][1].split()[0])
    egg['egg_group'] = even_more_info['Egg Groups']
    
    pokemon['egg'] = egg
    
    effort_values = {}
    form = 'Normal Form'
    
    for value in more_info['Effort Values Earned']:
        if re.search(r'\d', value):
            s = value.split()
            effort_values.setdefault(form, []).append({ 'type': s[1], 'value': int(s[0])})
        else:
            form = value
    
    pokemon['effort_values'] = effort_values
    
    '''
    corrigir experience_growth
    '''
    
    if even_more_info['Wild Hold Item'] == '':
        pokemon['wild_hold_item'] = {}
    else:
        item_split = even_more_info['Wild Hold Item'].split(' - ')
    
        pokemon['wild_hold_item'] = { 'item': item_split[0], 'percentage': int(item_split[1].split('%')[0]) }
    
    
    return pokemon

def get_pokemon_data(pokemon):
    soup = BeautifulSoup(pokemon, 'html.parser')
    pokemon_info = soup.find('a', {'name': 'general'}).find_all_next('table', class_='dextable')
    
    pictures = get_poke_pictures(pokemon_info[0])
    # separo pesos e alturas?
    info = get_poke_info(pokemon_info[1])
    more_info = get_poke_more_info(pokemon_info[2])
    
    i = 3
    weakness = get_poke_weakness(pokemon_info[i])
    i += 1        
    
    even_more_info = get_poke_even_more_info(pokemon_info[i])
    i += 1
    # evolution_chain = get_evolution_chain(pokemon_info[i])
    #está mal, resolver
    i += 1
    hasGenderDifferences, gender_differences = get_poke_gender_differences(pokemon_info[i])
    
    if hasGenderDifferences:
        i += 1
    
    hasAlternate, alternate_forms = get_poke_alternate_forms(pokemon_info[i])
    
    if hasAlternate:
        i += 3
    else:
        i += 2
        
    hasLevelMoves = True
    level_moves = {}
    while hasLevelMoves:
        hasLevelMoves, moves = get_poke_level_moves(pokemon_info[i])
        if hasLevelMoves:
            for form in moves:
                level_moves[form] = moves[form]
            i += 1
            
    hasTM, tm_moves = get_poke_tm_moves(pokemon_info[i])
    if hasTM:
        i += 1
   
    hasEggMoves, egg_moves = get_poke_egg_moves(pokemon_info[i])
    
    if hasEggMoves:
        i += 1
        
    hasMoveReminder, reminder_moves = get_poke_reminder_moves(pokemon_info[i])
    
    if hasMoveReminder:
        i += 1
        
    hasSpecialMoves, special_moves = get_poke_special_moves(pokemon_info[i])
    
    if hasSpecialMoves:
        i += 1
        
    hasPreEvoMoves, pre_evo_moves = get_poke_pre_evo_moves(pokemon_info[i])
    
    if hasPreEvoMoves:
        i += 1
        
    stats = []
    while i < len(pokemon_info):
        stats.append(get_poke_stats(pokemon_info[i]))
        i += 1
    
    moves = {}
    moves['level_moves'] = level_moves
    moves['tm_moves'] = tm_moves
    moves['egg_moves'] = egg_moves
    moves['reminder_moves'] = reminder_moves
    moves['special_moves'] = special_moves
    moves['pre_evolve_moves'] = pre_evo_moves
    
    pokemon = join_data(pictures, info, more_info, even_more_info, weakness, gender_differences, alternate_forms, moves, stats)
    
    # print(pokemon)
    
    # print(pictures)
    # print('\n')
    # print(info)
    # print('\n')
    # print(more_info)
    # print('\n')
    # print(weakness)
    # print('\n')
    # print(even_more_info)
    # # print('\n')
    # # print(evolution_chain)
    # if hasGenderDifferences:
    #     print('\n')
    #     print(gender_differences)
    # if hasAlternate:
    #     print('\n')
    #     print(alternate_forms)
    # print('\n')
    # print(level_moves)
    # print('\n')
    # print(tm_moves)
    # if hasEggMoves:
    #     print('\n')
    #     print(egg_moves)
    # if hasMoveReminder:
    #     print('\n')
    #     print(reminder_moves)
    # if hasSpecialMoves:
    #     print('\n')
    #     print(special_moves)
    # if hasPreEvoMoves:
    #     print('\n')
    #     print(pre_evo_moves)
    # print('\n')
    # print(stats)
    
    return pokemon




def loadPokemons():
    main_page_url = f"{base_url}/pokedex-sv"
    main_page = get_html_from_url(main_page_url)

    types_pages = get_all_types_pages(main_page)

    pokemons = []
    for type_page in types_pages:
        page = get_html_from_url(type_page)
        pokemons.extend(get_all_pokemon_from_page(page))

    pokemons = list(set(pokemons))

    i = 1
    loadedPokemons = []
    for pokemon in pokemons:
        print(len(pokemons) - i, ' - ', pokemon)
        i += 1
        poke = get_html_from_url(pokemon)
        loadedPokemons.append(get_pokemon_data(poke))
    
    return loadedPokemons
    

# poke = get_html_from_url('https://www.serebii.net/pokedex-sv/muk')
# get_pokemon_data(poke)




