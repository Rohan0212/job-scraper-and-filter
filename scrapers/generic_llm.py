import os
import json
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

MODEL = "anthropic/claude-3-haiku"

def scrape_with_llm(url: str, html: str, base_url: str):
    soup = BeautifulSoup(html, 'html.parser')
    main_content = soup.find("main") or soup.body or soup
    html_content = str(main_content)

    prompt = f"""
You are a precise extractor. Only return jobs explicitly listed in the HTML of this page.
Do NOT infer or hallucinate job titles. Use exact text as shown on the page.
Return a JSON array with:
- "title" (exact)
- "location" (or "Remote" / "Unknown" if missing)
- "url" (full job description page, absolute URL)

Only return JSON. No markdown, no comments.

HTML:
{html_content}
"""

    try:
        chat_completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0
        )

        content = chat_completion.choices[0].message.content.strip()
        content = content.replace("```json", "").replace("```", "").strip()

        job_list = json.loads(content)
        results = []

        for job in job_list:
            title = job.get("title", "").strip()
            location = job.get("location", "Unknown").strip()
            job_url = urljoin(base_url, job.get("url", "").strip())
            if title and job_url:
                results.append((title, location, job_url))

        return results

    except Exception as e:
        print(f"[ERROR] LLM scraping failed: {e}")
        return []
