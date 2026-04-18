import requests
from bs4 import BeautifulSoup

def extract_text(url):
    try:
        r = requests.get(url, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")

        for t in soup(["script", "style"]):
            t.decompose()

        return " ".join(p.get_text() for p in soup.find_all("p"))[:2000]

    except:
        return ""
