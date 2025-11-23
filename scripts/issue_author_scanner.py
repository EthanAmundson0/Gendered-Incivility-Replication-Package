import requests
import csv
import time
from datetime import datetime

INPUT_CSV = "issue_threads.csv"
OUTPUT_CSV = "issue_authors.csv"

# Put GitHub token here
TOKEN = ""

HEADERS = {"Authorization": f"token {TOKEN}"}

def log(message):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

def get_issue_author(issue_url):
    response = requests.get(issue_url, headers=HEADERS)
    if response.status_code != 200:
        log(f"Error fetching {issue_url}")
        return None
    
    issue = response.json()
    user = issue.get("user")
    if not user:
        return None
    
    user_url = user["url"]
    r_user = requests.get(user_url, headers=HEADERS)
    if r_user.status_code != 200:
        log(f"Error fetching user {user_url}")
        return {
            "login": user.get("login"),
            "id": user.get("id"),
            "name": None,
            "location": None,
        }

    user_details = r_user.json()
    return {
        "login": user_details.get("login"),
        "id": user_details.get("id"),
        "name": user_details.get("name"),
        "location": user_details.get("location"),
    }

if __name__ == "__main__":
    with open(INPUT_CSV, newline='', encoding="utf-8") as infile, \
         open(OUTPUT_CSV, "w", newline='', encoding="utf-8") as outfile:
        
        reader = csv.DictReader(infile)
        fieldnames = ["issue_id", "login", "id", "name", "location"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for count, row in enumerate(reader, start=1):
            issue_id = row["issue_id"]
            issue_url = row["url"]

            log(f"Processing issue {issue_id} (#{count})")
            author_data = get_issue_author(issue_url)
            if author_data:
                author_data["issue_id"] = issue_id
                writer.writerow(author_data)
            
            time.sleep(1)