from urllib.parse import urljoin

def scrape_ashby(soup, base_url):
    """Scrape job listings from Ashby career pages."""
    jobs = []
    for div in soup.select("div[data-testid='job-listing']"):
        title_el = div.select_one("h3")
        link_el = div.select_one("a")
        loc_el = div.select_one("span[class*='location']")

        title = title_el.text.strip() if title_el else "Unknown"
        link = urljoin(base_url, link_el['href']) if link_el else base_url
        location = loc_el.text.strip() if loc_el else "Unknown"

        if title and link:
            jobs.append((title, location, link))
    return jobs
