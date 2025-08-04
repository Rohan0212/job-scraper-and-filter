from urllib.parse import urljoin
from scrapers.utils import extract_visible_text

def scrape_lever(soup, base_url):
    jobs = []
    page = 1

    while True:
        postings = soup.select('div.posting')
        for post in postings:
            title_el = post.select_one('.posting-title')
            link_el = post.select_one('a')
            loc_el = post.select_one('.posting-categories > span')

            title = title_el.text.strip() if title_el else "Unknown"
            link = urljoin(base_url, link_el['href']) if link_el else base_url
            location = loc_el.text.strip() if loc_el else "Unknown"

            if title and link:
                jobs.append((title, location, link))

        # Detect next page (if applicable)
        next_page = soup.select_one('a[rel="next"]')
        if next_page:
            next_url = urljoin(base_url, next_page['href'])
            soup, _ = extract_visible_text(next_url)
            if not soup:
                break
        else:
            break

    return jobs
