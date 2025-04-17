from scraper import EmailScraper
from search import get_top_urls
import csv
import os
import re

# 🔧 Turn keyword into clean filename
def sanitize_filename(keyword):
    return re.sub(r'\W+', '_', keyword.strip().lower())

# 💾 Save emails to keyword-based CSV file
def save_emails_to_csv(emails, keyword):
    filename = f"output/{sanitize_filename(keyword)}.csv"
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Email"])
        for email in sorted(emails):
            writer.writerow([email])

    print(f"\n✅ Saved {len(emails)} emails to {filename}")
    return filename  # ✅ Return path for Flask to download

# 📁 Persistent history file
HISTORY_FILE = "output/email_history.txt"

# ⚙️ This is the core function Flask will call
def run_scraper(keyword, goal=20):
    all_emails = set()
    urls_seen = set()
    url_offset = 0

    # Load global history of past emails
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            previous_emails = set(line.strip() for line in f)
    else:
        previous_emails = set()

    while len(all_emails) < goal:
        urls = get_top_urls(keyword, limit=20 + url_offset)
        urls = [url for url in urls if url not in urls_seen]

        if not urls:
            break

        for url in urls:
            urls_seen.add(url)
            scraper = EmailScraper(base_url=url, max_pages=10)
            new_emails = scraper.scrape()

            # 🧹 Filter already-known emails
            filtered_emails = new_emails - previous_emails - all_emails
            all_emails.update(filtered_emails)

            if len(all_emails) >= goal:
                break

        url_offset += 20

    if all_emails:
        # Save to CSV
        filepath = save_emails_to_csv(all_emails, keyword)

        # 📌 Update global history
        with open(HISTORY_FILE, "a", encoding="utf-8") as f:
            for email in sorted(all_emails):
                f.write(email + "\n")

        return {"emails": list(sorted(all_emails)), "file": os.path.basename(filepath)}
    else:
        return {"emails": [], "file": None}

# 🧪 CLI Mode (still works!)
if __name__ == "__main__":
    print("🔍 Advanced Email Scraper 🔥\n")
    keyword = input("Enter a keyword to Google: ").strip()
    result = run_scraper(keyword)
    if result["emails"]:
        print(f"\n✅ Collected {len(result['emails'])} emails.")
    else:
        print("❌ No emails found.")
