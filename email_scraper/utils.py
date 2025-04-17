import re

# Email regex pattern (catch most formats)
EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"

# Garbage domains we want to skip
BLACKLISTED_DOMAINS = [
    "noreply", "no-reply", "example", "localhost"
]

def extract_emails(text):
    raw_emails = re.findall(EMAIL_REGEX, text)
    return set(filter(is_valid_email, raw_emails))

def is_valid_email(email, allowed_domains=None):
    if allowed_domains is None:
        allowed_domains = [".com"]

    # Filter out garbage domains
    for word in BLACKLISTED_DOMAINS:
        if word in email.lower():
            return False

    # Make sure it ends with allowed domain suffixes
    return any(email.lower().endswith(domain) for domain in allowed_domains)
