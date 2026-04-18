from duckduckgo_search import DDGS

def search_web(query):
    results = []

    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=5):
            results.append({"url": r["href"]})

    return results
