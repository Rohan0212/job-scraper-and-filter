# job_page_classifier.py
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import openai
from openai import OpenAI

import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# Load OpenRouter API key from .env
load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

MODEL = "anthropic/claude-3-haiku"
OUTPUT_CSV = "classified_links_updated.csv"

def extract_visible_text_with_playwright(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=45000)
            page.wait_for_timeout(5000)

            # Scroll to bottom to load dynamic content
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(3000)

            content = page.content()
            browser.close()

        soup = BeautifulSoup(content, 'html.parser')
        for tag in soup(['script', 'style', 'noscript', 'meta', 'link']):
            tag.decompose()

        keywords_text = []
        job_keywords = [
            'open position', 'job', 'role', 'apply now', 'career',
            'opportunity', 'we’re hiring', 'join our team', 'see openings',
            'view all jobs', 'browse jobs', 'join us'
        ]

        for tag in soup.find_all(['a', 'button', 'div', 'span', 'h2', 'h3']):
            text = tag.get_text(strip=True).lower()
            if any(keyword in text for keyword in job_keywords):
                keywords_text.append(text)

        full_text = soup.get_text(separator=' ', strip=True)
        truncated = full_text[:7000]

        combined_text = "\n".join(keywords_text) + "\n" + truncated
        return combined_text[:8000]

    except Exception as e:
        print(f"[ERROR] Could not fetch {url}: {e}")
        return None


def ask_claude_if_job_page(text):
    prompt = f"""
You are a helpful assistant. Your task is to classify whether a given web page likely contains **actual job openings or career opportunities**.

✅ Classify as "Yes" if:
- The page contains job titles, links to open roles, or job categories (even if they are not visible without clicking)
- Or if it contains a section with "View Open Positions", "Browse Jobs", "Apply Now" etc. that suggests jobs are listed

🚫 Classify as "No" if:
- The page only talks about company culture, perks, or values with no links or listings
- Or if it is a generic contact page, blog, or unrelated content

### Input:
{text}

Answer only **Yes** or **No**.
"""

    try:
        response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=5,
        temperature=0,
        )

        answer = response.choices[0].message.content.strip()
        if answer.lower().startswith("yes"):
            return "Yes"
        elif answer.lower().startswith("no"):
            return "No"
        else:
            return "Unclear"

    except Exception as e:
        print(f"[ERROR] OpenRouter Claude failed: {e}")
        return "Error"


def classify_links(csv_path):
    df = pd.read_csv(csv_path)
    results = []

    for idx, row in df.iterrows():
        domain = row['domain']
        link = row['career_link']
        print(f"[CLASSIFYING] {domain} → {link}")

        verdict = "Error"
        text = extract_visible_text_with_playwright(link)

        if text:
            verdict = ask_claude_if_job_page(text)
        else:
            verdict = "Fetch Failed"

        results.append({"domain": domain, "career_link": link, "has_jobs": verdict})
        time.sleep(1.5)  # Rate-limit

    classified_df = pd.DataFrame(results)
    classified_df.to_csv(OUTPUT_CSV, index=False)
    print(f"\n✅ Saved results to {OUTPUT_CSV}")


if __name__ == "__main__":
    classify_links("career_links1.csv")

