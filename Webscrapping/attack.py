from bs4 import BeautifulSoup
from utils import get_html_from_url, base_url


def get_all_attack_types_pages(main_page):
    soup = BeautifulSoup(main_page, 'html.parser')
    type_group = soup.select_one("p:-soup-contains('Attacks by Type')").find("div").find_all("td")
    types_pages = []
    for type_line in type_group:
         types_pages.extend([f"{base_url}{t['href']}" for t in type_line.find_all("a")])
    return types_pages

def get_all_pokemon_from_page(page):
    soup = BeautifulSoup(page, 'html.parser')
    pokemons_entrys = soup.select_one("p:-soup-contains('The Pokémon below are the Pokémon of the')").find_all("table")

    return [f"{base_url}{pokemon_entry.find('a')['href']}" for pokemon_entry in pokemons_entrys[1:]]

main_attack_page_url = f"{base_url}/attackdex-sv"
main_page = get_html_from_url(main_attack_page_url)
attack_types = get_all_attack_types_pages(main_page)
print(attack_types)
