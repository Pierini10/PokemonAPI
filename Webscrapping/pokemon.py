import urllib.request
from bs4 import BeautifulSoup

base_url = "https://www.serebii.net"

def get_html_from_url(url):
    page = urllib.request.urlopen(url)
    html = page.read().decode("ISO-8859-1")
    page.close()
    return html

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

main_page_url = f"{base_url}/pokedex-sv"
main_page = get_html_from_url(main_page_url)

types_pages = get_all_types_pages(main_page)

pokemons = []
for type_page in types_pages:
    page = get_html_from_url(type_page)
    pokemons.extend(get_all_pokemon_from_page(page))

print(len(pokemons))



