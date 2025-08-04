from urllib.parse import urljoin
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_workday(driver, base_url):
    """Scrape job listings from Workday career pages."""
    jobs = []
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-automation-id='jobTitle']"))
        )

        while True:
            job_elements = driver.find_elements(By.CSS_SELECTOR, "div[data-automation-id='jobTitle']")
            for element in job_elements:
                try:
                    title = element.text.strip() or "Unknown"
                    link_element = element.find_element(By.XPATH, "./ancestor::a")
                    job_url = urljoin(base_url, link_element.get_attribute("href"))
                    location_element = element.find_element(By.XPATH, "./following::div[contains(@data-automation-id, 'location')]")
                    location = location_element.text.strip() if location_element else "Unknown"

                    if title and job_url:
                        jobs.append((title, location, job_url))
                except Exception as e:
                    print(f"[WARN] Skipping job due to error: {e}")

            try:
                next_button = driver.find_element(By.CSS_SELECTOR, "button[data-automation-id='nextPage']")
                if next_button.is_enabled():
                    next_button.click()
                    time.sleep(2)
                else:
                    break
            except:
                break

    except Exception as e:
        print(f"[ERROR] Workday scraping failed: {e}")
    finally:
        if driver:
            driver.quit()

    return jobs
