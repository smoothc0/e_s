import os

class Config:
    # Request headers
    HEADERS = {
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Scraping settings
    DELAY = 1  # seconds between requests
    MAX_PAGES = 10  # maximum pages to scrape per site
    
    # API keys (set via environment variables)
    SERPAPI_KEY = os.getenv("5de591cfb44477e356c85e44654b578ed13cad5e2287cea4774d55704b628216", "")
    
    # Email validation
    ALLOWED_DOMAINS = [".com", ".org", ".net", ".io", ".co"]
    BLACKLISTED_DOMAINS = [
        "noreply", "no-reply", "example", 
        "localhost", "domain", "test"
    ]

# Create config instance
config = Config()