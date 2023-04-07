import urllib.request

base_url = "https://www.serebii.net"

def get_html_from_url(url):
    page = urllib.request.urlopen(url)
    html = page.read().decode("ISO-8859-1")
    page.close()
    return html

def process_int(value):
    value = value.text.strip()
    if value == "--":
        return 0
    return int(value)

def process_img_url(value):
    return value.find("img")["src"].split("/")[-1].split(".")[0].upper()