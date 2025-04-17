import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
from utils import extract_emails
from config import HEADERS, DELAY

class EmailScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.ua = UserAgent()

    def scrape_with_sources(self):
        email_to_source = {}

        print(f"[+] Scraping: {self.base_url}")
        try:
            headers = HEADERS.copy()
            headers['User-Agent'] = self.ua.random

            response = requests.get(self.base_url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            new_emails = extract_emails(soup.text)
            for email in new_emails:
                if email not in email_to_source:
                    email_to_source[email] = self.base_url

            time.sleep(DELAY)

        except Exception as e:
            print(f"[!] Failed: {self.base_url} — {e}")

        return email_to_source
