from bs4 import BeautifulSoup
from .utils import get_html_from_url, base_url
from ..models.ability import create_ability


def get_all_abilities_pages(main_page):
    soup = BeautifulSoup(main_page, 'html.parser')
    pages = []
    for ability_page in soup.find_all("option"):
        if ability_page["value"] != "index.shtml":
            pages.append(f"{base_url}{ability_page['value']}")
    return pages

def get_all_ability_from_page(page):
    soup = BeautifulSoup(page, 'html.parser')
    ability_table = soup.find_all("table", class_="dextable")[1]
    ability_name = ability_table.find("td", class_="cen").text.strip()
    header = ability_table.find_all("td", class_="fooevo")
    other = ability_table.find_all("td", class_="fooinfo")
    ability_description = other[0].text.strip()
    ability_in_deth_description = other[1].text.strip() if len(header) > 1 and header[1].text.strip() == "In-Depth Effect:" else ""
    return create_ability(ability_name, ability_description, ability_in_deth_description)


def load_all_ability():
    main_attack_page_url = f"{base_url}/abilitydex"
    main_page = get_html_from_url(main_attack_page_url)
    abilities_pages = get_all_abilities_pages(main_page)
    return [get_all_ability_from_page(get_html_from_url(ability_page)) for ability_page in abilities_pages]
