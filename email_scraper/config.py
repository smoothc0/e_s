import os

class Config:
    # Headers for requests
    HEADERS = {
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
        "Connection": "keep-alive"
    }

    # Delay between requests (in seconds)
    DELAY = 1

    # SerpAPI key from environment
    SERPAPI_KEY = os.environ.get("5de591cfb44477e356c85e44654b578ed13cad5e2287cea4774d55704b628216", "")

    # Security
    ALLOWED_EMAIL_DOMAINS = [".com", ".org", ".net", ".io"]
    BLACKLISTED_DOMAINS = [
        "noreply", "no-reply", "example", "localhost", 
        "domain", "test", "mailinator"
    ]