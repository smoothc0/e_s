from serpapi import GoogleSearch
from config import SERPAPI_KEY

def get_top_urls(keyword, limit=10):
    search = GoogleSearch({
        "q": keyword,
        "api_key": SERPAPI_KEY,
        "num": limit
    })
    
    results = search.get_dict()
    organic = results.get("organic_results", [])
    
    urls = []
    for result in organic:
        link = result.get("link")
        if link:
            urls.append(link)
    
    return urls
