import urllib.request

base_url = "https://www.serebii.net"

def get_html_from_url(url):
    page = urllib.request.urlopen(url)
    html = page.read().decode("ISO-8859-1")
    page.close()
    return html