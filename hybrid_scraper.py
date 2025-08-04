from scrapers.platform_detector import detect_platform
from scrapers.greenhouse import scrape_greenhouse
from scrapers.lever import scrape_lever
from scrapers.workday import scrape_workday
from scrapers.generic_llm import scrape_with_llm
from quality_filter import filter_jobs

import pandas as pd
import time

def main():
    df = pd.read_csv("classified_links_updated.csv")
    all_jobs = []

    for _, row in df.iterrows():
        if str(row['has_jobs']).strip().lower() != "yes":
            continue

        company = row['domain']
        link = row['career_link']

        print(f"\n[SCRAPING] {company} → {link}")

        try:
            platform, soup, html = detect_platform(link)

            if platform == "greenhouse":
                jobs = scrape_greenhouse(soup, link)
            elif platform == "lever":
                jobs = scrape_lever(soup, link)
            elif platform == "workday":
                jobs = scrape_workday(soup, link)
            else:
                jobs = scrape_with_llm(link, html, link)

            for title, location, job_url in jobs:
                all_jobs.append({
                    "Company": company,
                    "Job Title": title,
                    "Location": location,
                    "URL": job_url
                })

        except Exception as e:
            print(f"[ERROR] Failed on {company}: {e}")

        time.sleep(1.5)

    # ✅ Filtering step added here
    print(f"\n[INFO] Raw jobs scraped: {len(all_jobs)}")

    from quality_filter import filter_jobs
    filtered_jobs = filter_jobs(all_jobs, min_score=3)

    print(f"[INFO] Jobs after quality filtering: {len(filtered_jobs)}")

    # Save filtered jobs
    df_out = pd.DataFrame(filtered_jobs)
    df_out.to_csv("new_all_jobs_filtered.csv", index=False)
    print(f"\n✅ Done. {len(df_out)} high-quality jobs saved.")

if __name__ == "__main__":
    main()
