import re
from pathlib import Path
from config import Config
from email_scraper.config import config  # updated import

def is_valid_email(email):
    """Validate email against config rules"""
    email = email.lower()
    
    # Check blacklisted domains
    if any(blacklisted in email for blacklisted in config.BLACKLISTED_DOMAINS):
        return False
        
    # Check allowed domains
    if not any(email.endswith(domain) for domain in config.ALLOWED_DOMAINS):
        return False
        
    return True

def sanitize_filename(keyword):
    """Convert keyword to safe filename"""
    return re.sub(r'\W+', '_', keyword.strip().lower())

def extract_emails(text):
    """Extract emails from text using regex"""
    email_regex = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    raw_emails = re.findall(email_regex, text)
    return set(filter(is_valid_email, raw_emails))

def is_valid_email(email):
    """Validate email against config rules"""
    email = email.lower()
    config = Config()
    
    # Check blacklisted domains
    if any(blacklisted in email for blacklisted in config.BLACKLISTED_DOMAINS):
        return False
        
    # Check allowed domains
    if not any(email.endswith(domain) for domain in config.ALLOWED_EMAIL_DOMAINS):
        return False
        
    return True