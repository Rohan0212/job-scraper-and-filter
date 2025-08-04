import requests
from bs4 import BeautifulSoup

def extract_visible_text(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(resp.text, 'html.parser')

        for tag in soup(['script', 'style', 'noscript', 'meta', 'link']):
            tag.decompose()

        return soup, soup.get_text(separator=' ', strip=True)
    except Exception as e:
        print(f"[ERROR] Failed to extract from {url}: {e}")
        return None, None
