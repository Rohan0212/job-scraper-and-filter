# career_link_crawler.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import csv
import sys

def find_possible_career_links(domain):
    base_url = f"https://{domain}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        resp = requests.get(base_url, headers=headers, timeout=10)
        if resp.status_code != 200:
            print(f"[ERROR] Failed to load {base_url}: {resp.status_code}")
            return domain, []

        soup = BeautifulSoup(resp.text, 'html.parser')
        links = []

        for a in soup.find_all('a', href=True):
            href = a['href'].strip()
            text = a.get_text(strip=True).lower()
            full_url = urljoin(base_url, href)

            # Check for common career/job keywords in href or anchor text
            if re.search(r'(careers?|jobs?|work|join|hire)', href.lower()) or \
               re.search(r'(careers?|jobs?|we\'?re hiring|open roles)', text):
                if domain in urlparse(full_url).netloc:
                    links.append(full_url)
        # 🔷 ADD FALLBACK PATHS HERE
        FALLBACK_PATHS = [
            "/careers",
            "/careers/jobs",
            "/careers/open-positions",
            "/jobs",
            "/about/careers"
        ]

        for path in FALLBACK_PATHS:
            fallback_url = urljoin(base_url, path)
            links.append(fallback_url)

        return domain, list(set(links))  # Remove duplicates

    except Exception as e:
        print(f"[ERROR] Exception for {domain}: {e}")
        return domain, []

def load_domains_from_file(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def save_links_to_csv(results, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['domain', 'career_link'])
        writer.writeheader()
        for domain, links in results:
            for link in links:
                writer.writerow({'domain': domain, 'career_link': link})

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python career_link_crawler.py domains.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = "career_links1.csv"

    domains = load_domains_from_file(input_file)
    results = [find_possible_career_links(domain) for domain in domains]
    save_links_to_csv(results, output_file)

    print(f"\n[SUCCESS] Saved career links to {output_file}")
