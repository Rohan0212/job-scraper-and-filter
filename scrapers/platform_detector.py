from bs4 import BeautifulSoup
import requests

def extract_html(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    return soup, resp.text

def detect_platform(url):
    soup, html = extract_html(url)

    if soup.select("div.opening"):
        platform = "greenhouse"
    elif soup.select("div.posting"):
        platform = "lever"
    elif soup.find(text=lambda t: t and "workday" in t.lower()):
        platform = "workday"
    else:
        platform = "unknown"

    print(f"[INFO] Detected platform: {platform}")
    return platform, soup, html
