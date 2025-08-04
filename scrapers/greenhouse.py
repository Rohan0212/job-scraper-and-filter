from urllib.parse import urljoin
from scrapers.utils import extract_visible_text

def scrape_greenhouse(soup, base_url):
    jobs = []
    for div in soup.select('div.opening'):
        title = div.a.text.strip()
        link = urljoin(base_url, div.a['href'])
        location = div.select_one('.location').text.strip() if div.select_one('.location') else "N/A"
        jobs.append((title, location, link))
    return jobs
def scrape_greenhouse(soup, base_url):
    jobs = []
    page = 1

    while True:
        openings = soup.select('div.opening')
        for div in openings:
            title = div.a.text.strip()
            link = urljoin(base_url, div.a['href'])
            location = div.select_one('.location').text.strip() if div.select_one('.location') else "Unknown"
            jobs.append((title, location, link))

        next_link = soup.select_one('a.next_page')
        if next_link and 'disabled' not in next_link.get('class', []):
            next_url = urljoin(base_url, next_link['href'])
            soup, _ = extract_visible_text(next_url)
            if not soup:
                break
        else:
            break

    return jobs
