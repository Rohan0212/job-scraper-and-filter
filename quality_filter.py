import pandas as pd

# Define lists of phrases that indicate a "fake" job title
NON_JOB_KEYWORDS = [
    "life at", "our opportunity", "benefits", "university", "opportunistic",
    "set a trigger", "connect to anything", "write custom logic",
    "deploy in one click", "scheduled jobs", "notifications", "etl",
    "human-in-the-loop", "granular debugging", "secure by default",
    "permissions", "deploy on-prem", "announcement", "teams", "loading",
    "learn more", "view jobs", "browse jobs", "tips for applying",
    "career growth", "talent community", "awards", "explore opportunities",
    "your chance to join", "make an impact", "dream big", "ownership",
    "growth mindset", "current openings", "working at", "hiring & onboarding",
    "women of", "open positions", "candidate resources hub",
    "interviewing", "career growth", "benefits and perks", "tagging",
    "autosave", "embedded widgets", "join the future", "monday", "mailchimp"
]

def looks_like_real_job(title):
    """Return True if the title looks like a real job posting."""
    if not isinstance(title, str):
        return False

    t = title.strip().lower()

    if not t or len(t) < 3:
        return False

    # Reject if contains obvious non-job text
    if any(kw in t for kw in NON_JOB_KEYWORDS):
        return False

    # Accept if contains common job words
    job_keywords = [
        "engineer", "developer", "designer", "manager", "specialist", 
        "scientist", "analyst", "consultant", "intern", "lead", "director",
        "associate", "architect", "administrator", "coordinator", "recruiter",
        "accountant", "officer", "technician", "sales", "marketing", "finance",
        "counsel", "attorney", "support", "customer", "executive", "product"
    ]
    if any(word in t for word in job_keywords):
        return True

    return False


def filter_jobs(input_csv, output_csv, rejected_csv):
    df = pd.read_csv(input_csv)
    accepted, rejected = [], []

    for _, row in df.iterrows():
        title = str(row.get("Job Title", "")).strip()
        location = str(row.get("Location", "")).strip()

        reasons = []

        # Title filter
        if not looks_like_real_job(title):
            reasons.append("Non-job title")

        # Location filter
        if not location or location.lower() in ["unknown", "n/a", "none"]:
            reasons.append("Unknown location")

        if reasons:
            job_dict = row.to_dict()
            job_dict["Rejected Because"] = "; ".join(reasons)
            rejected.append(job_dict)
        else:
            accepted.append(row.to_dict())

    # Save results
    pd.DataFrame(accepted).to_csv(output_csv, index=False)
    pd.DataFrame(rejected).to_csv(rejected_csv, index=False)

    print(f"[INFO] Total jobs in input: {len(df)}")
    print(f"[INFO] Jobs accepted: {len(accepted)}")
    print(f"[INFO] Jobs rejected: {len(rejected)}")
    print(f"✅ Saved filtered jobs to {output_csv}")
    print(f"⚠️ Saved rejected jobs to {rejected_csv}")


if __name__ == "__main__":
    filter_jobs(
        input_csv="new_all_jobs.csv",
        output_csv="new_all_jobs_filtered.csv",
        rejected_csv="rejected_jobs.csv"
    )
