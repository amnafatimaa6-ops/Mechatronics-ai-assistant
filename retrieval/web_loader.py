import requests
from bs4 import BeautifulSoup

def extract_text(url):
    try:
        r = requests.get(url, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")

        for tag in soup(["script", "style", "nav"]):
            tag.decompose()

        text = " ".join(p.get_text() for p in soup.find_all("p"))

        return text[:2500]

    except:
        return ""
