import requests
from bs4 import BeautifulSoup

def extract_text(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        # remove junk
        for tag in soup(["script", "style", "nav"]):
            tag.decompose()

        text = " ".join(p.get_text() for p in soup.find_all("p"))

        return text[:2000]  # limit noise

    except:
        return ""
