from bs4 import BeautifulSoup
from .utils import get_html_from_url, base_url, process_img_url, process_int
from ..models.attack import AttactCategory, create_attack


def get_all_attack_types_pages(main_page):
    soup = BeautifulSoup(main_page, 'html.parser')
    types_pages = []
    for category in AttactCategory.ALL:
        url = soup.find('a', href=f"{category.lower()}.shtml")["href"]
        types_pages.append(f"{base_url}/attackdex-sv/{url}")
    return types_pages

def get_all_attacks_from_page(page):
    soup = BeautifulSoup(page, 'html.parser')
    attacks = soup.find("table", class_="dextable").find_all("tr")[1:]
    processed_attacks = []
    for attack in attacks:
        attack_vars = attack.find_all("td")
        attack_name = attack_vars[0].find("a").text.strip()
        attack_type = process_img_url(attack_vars[1])
        attack_category = process_img_url(attack_vars[2])
        attack_pp = process_int(attack_vars[3])
        attack_damage = process_int(attack_vars[4])
        attack_accuracy = process_int(attack_vars[5])
        attack_effect = attack_vars[6].text.strip()
        processed_attacks.append(create_attack(attack_name, attack_type, attack_category, attack_pp, attack_damage, attack_accuracy, attack_effect))

    return processed_attacks


def load_all_attacks():
    main_attack_page_url = f"{base_url}/attackdex-sv"
    main_page = get_html_from_url(main_attack_page_url)
    attacks_pages = get_all_attack_types_pages(main_page)
    attacks = []
    for attacks_page in attacks_pages:
        page = get_html_from_url(attacks_page)
        attacks.extend(get_all_attacks_from_page(page))
    return attacks
