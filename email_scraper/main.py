from scraper import EmailScraper
from search import get_top_urls
import csv
import os
import re

HISTORY_PATH = "output/email_history.txt"

def sanitize_filename(keyword):
    return re.sub(r'\W+', '_', keyword.strip().lower())

def load_history():
    if not os.path.exists(HISTORY_PATH):
        return set()
    with open(HISTORY_PATH, "r", encoding="utf-8") as f:
        return set(line.strip().split(",")[0] for line in f if line.strip())

def update_history(email_source_pairs):
    os.makedirs(os.path.dirname(HISTORY_PATH), exist_ok=True)
    with open(HISTORY_PATH, "a", encoding="utf-8") as f:
        for email, source in email_source_pairs:
            f.write(f"{email},{source}\n")

def save_emails_to_csv(email_source_pairs, keyword):
    filename = f"output/{sanitize_filename(keyword)}.csv"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Email", "Source"])
        for email, source in sorted(email_source_pairs):
            writer.writerow([email, source])
    print(f"\n✅ Saved {len(email_source_pairs)} emails to {filename}")
    return filename

def clear_history():
    if os.path.exists(HISTORY_PATH):
        os.remove(HISTORY_PATH)
        print("🧹 Cleared email history.")
    else:
        print("📭 No history to clear.")

def run_scraper(keyword, goal=20):
    history = load_history()
    all_emails = {}
    urls_seen = set()
    url_offset = 0

    while len(all_emails) < goal:
        urls = get_top_urls(keyword, limit=20 + url_offset)
        urls = [url for url in urls if url not in urls_seen]
        if not urls:
            break

        for url in urls:
            urls_seen.add(url)
            scraper = EmailScraper(base_url=url)  # Simplified constructor
            emails = scraper.scrape_with_sources()
            for email in emails:
                if email not in history and email not in all_emails:
                    all_emails[email] = url
                if len(all_emails) >= goal:
                    break
            if len(all_emails) >= goal:
                break
        url_offset += 20

    if all_emails:
        email_source_pairs = list(all_emails.items())
        update_history(email_source_pairs)
        filepath = save_emails_to_csv(email_source_pairs, keyword)
        return {"emails": email_source_pairs, "file": f"{sanitize_filename(keyword)}.csv"}
    else:
        return {"emails": [], "file": None}

if __name__ == "__main__":
    print("🔍 Advanced Email Scraper 🔥\n")
    keyword = input("Enter a keyword to Google: ").strip()
    result = run_scraper(keyword)
    if result["emails"]:
        print(f"\n✅ Collected {len(result['emails'])} emails.")
    else:
        print("❌ No emails found.")
