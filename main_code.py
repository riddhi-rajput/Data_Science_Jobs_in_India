import requests
import pandas as pd
import time

APP_ID = "b0a58858"
APP_KEY = "190a2c30812d5d168d936a31ab8856da"

BASE_URL = "https://api.adzuna.com/v1/api/jobs/in/search"

# 🔹 Roles you want to analyse
ROLES = [
    "data analyst",
    "business analyst",
    "data scientist",
    "product analyst"
]

RESULTS_PER_PAGE = 50
MAX_PAGES = 20          # 10 pages × 50 × 4 roles = ~2000 rows

rows = []

for role in ROLES:
    print(f"\n🔍 Fetching jobs for role: {role}")

    for page in range(1, MAX_PAGES + 1):
        params = {
            "app_id": "b0a58858",
            "app_key": "190a2c30812d5d168d936a31ab8856da",
            "results_per_page": RESULTS_PER_PAGE,
            "what": role,
            "content-type": "application/json"
        }

        print(f"  Page {page}")
        r = requests.get(f"{BASE_URL}/{page}", params=params)
        data = r.json()

        for job in data.get("results", []):
            rows.append({
                "search_role": role,   # 🔥 key addition
                "title": job.get("title"),
                "company": job.get("company", {}).get("display_name"),
                "location": job.get("location", {}).get("display_name"),
                "description": job.get("description"),
                "salary_min": job.get("salary_min"),
                "salary_max": job.get("salary_max"),
                "created": job.get("created"),
                "category": job.get("category", {}).get("label")
            })

        time.sleep(1)  # respect API limits

df = pd.DataFrame(rows)

# Optional: remove duplicates by title + company + location
df = df.drop_duplicates(subset=["title", "company", "location"])

df.to_csv("adzuna_jobs_india_multi_role.csv", index=False)

print("\n✅ Saved file: adzuna_jobs_india_multi_role.csv")
print("Final shape:", df.shape)
