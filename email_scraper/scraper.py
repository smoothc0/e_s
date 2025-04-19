import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from fake_useragent import UserAgent
import time
from utils import extract_emails
from config import HEADERS, DELAY

class EmailScraper:
    def __init__(self, base_url, max_pages=20):
        self.base_url = base_url
        self.visited = set()
        self.to_visit = [base_url]
        self.ua = UserAgent()
        self.max_pages = max_pages

    def scrape_with_sources(self):
        count = 0
        email_to_source = {}

        while self.to_visit and count < self.max_pages:
            url = self.to_visit.pop(0)
            if url in self.visited:
                continue

            print(f"[+] Scraping: {url}")
            try:
                headers = HEADERS.copy()
                headers['User-Agent'] = self.ua.random

                response = requests.get(url, headers=headers, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')

                new_emails = extract_emails(soup.text)
                for email in new_emails:
                    if email not in email_to_source:
                        email_to_source[email] = url

                for link in soup.find_all('a', href=True):
                    href = link['href']
                    full_url = urljoin(url, href)

                    if self._is_internal_link(full_url):
                        if full_url not in self.visited and full_url not in self.to_visit:
                            self.to_visit.append(full_url)

                self.visited.add(url)
                count += 1
                time.sleep(DELAY)

            except Exception as e:
                print(f"[!] Failed: {url} — {e}")

        return email_to_source

    def _is_internal_link(self, url):
        return urlparse(url).netloc == urlparse(self.base_url).netloc