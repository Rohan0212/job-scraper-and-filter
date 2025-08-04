# Job Scraper & Quality Filter

A Python project that **scrapes job postings from company career sites** and applies an intelligent **quality filter** to produce structured, recruiter‑ready datasets. 

The pipeline ensures that only real job opportunities (e.g., *Software Engineer*, *Product Manager*, *Data Analyst*) are retained while removing duplicates, irrelevant titles (e.g., *Life at Stripe*, *Benefits*, *Browse Jobs*), and incomplete postings (such as those with unknown locations).

---

## ✨ Features

- **Automated Job Scraping**  
  Collects job postings from career sites into a structured CSV.

- **Intelligent Filtering**  
  - Removes marketing fluff (e.g., *Benefits*, *Browse Jobs*).  
  - Keeps only valid job postings based on keywords like `Engineer`, `Manager`, `Designer`, etc.  
  - Discards postings with unknown or blank locations.  

- **Dual Output CSVs**  
  - `new_all_jobs_filtered.csv` → ✅ Clean, valid job postings.  
  - `rejected_jobs.csv` → ⚠️ Rejected entries with reasons.

---
## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/Rohan0212/job-scraper-and-filter.git
cd job-scraper-and-filter
```
### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
### 3. Run the Scraper
```bash
python hybrid_scraper.py
```
4. Apply Quality Filter
```bash
python quality_filter.py
```
## 📊 Sample Output
- **Filtered Jobs**
- **Rejected Jobs (with Reasons)**
