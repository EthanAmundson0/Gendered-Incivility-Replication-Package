import requests
import csv
import sys
import time
from datetime import datetime

csv.field_size_limit(sys.maxsize)

INPUT_CSV = "comments.csv"
OUTPUT_CSV = "comment_authors.csv"

# Put GitHub token here
TOKEN = ""

HEADERS = {"Authorization": f"token {TOKEN}"}

def log(message):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

def get_user(user_id):
    url = f"https://api.github.com/user/{user_id}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        log(f"Error fetching {user_id}")
        return {
            "user_id": user_id, 
            "login": None, 
            "name": None, 
            "location": None
            }
    
    data = response.json()
    return {
        "user_id": user_id,
        "login": data.get("login"),
        "name": data.get("name"),
        "location": data.get("location"),
    }

if __name__ == "__main__":
    # Read in comments from csv
    with open(INPUT_CSV, newline='', encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        comments = list(reader)

    # Get unique user_ids
    unique_user_ids = {row["user_id"] for row in comments}

    # Get each unique user's data
    user_data_map = {}
    for count, uid in enumerate(unique_user_ids, start=1):
        log(f"Getting user {uid} ({count}/{len(unique_user_ids)})")
        user_data_map[uid] = get_user(uid)

    # Write user data out
    with open(OUTPUT_CSV, "w", newline='', encoding="utf-8") as outfile:
        fieldnames = ["issue_id", "comment_id", "user_id", "login", "name", "location"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in comments:
            uid = row["user_id"]
            user_info = user_data_map.get(uid, {})
            writer.writerow({
                "issue_id": row["issue_id"],
                "comment_id": row["comment_id"],
                "user_id": uid,
                "login": user_info.get("login"),
                "name": user_info.get("name"),
                "location": user_info.get("location"),
            })
