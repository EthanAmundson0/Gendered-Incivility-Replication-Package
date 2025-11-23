from genderComputer import GenderComputer
import pandas as pd

gc = GenderComputer()

issue_authors_df = pd.read_csv('issue_authors.csv')
comment_authors_df = pd.read_csv('comment_authors.csv')
dataframe_maker = {'issue_id' : [],
                   'login' : [],
                   'id' : [],
                   'name': [],
                   'location' : [],
                   'gender' : []}
dataframe_maker_two = {'issue_id' : [],
                   'comment_id' : [],
                   'user_id' : [],
                   'login' : [],
                   'name': [],
                   'location' : [],
                   'gender' : []}

for index, data in issue_authors_df.iterrows():
    issue_id = data["issue_id"]
    login = data["login"]
    user_id = data["id"]

    name = "" if pd.isna(data["name"]) else str(data["name"])
    location = "" if pd.isna(data["location"]) else str(data["location"])
    country = "" if "country" in data and not pd.isna(data["country"]) else ""

    try:
        gender = gc.resolveGender(name, country)
    except Exception:
        gender = "unknown"

    dataframe_maker["issue_id"].append(issue_id)
    dataframe_maker["login"].append(login)
    dataframe_maker["id"].append(user_id)
    dataframe_maker["name"].append(name)
    dataframe_maker["location"].append(location)
    dataframe_maker["gender"].append(gender)

issue_authors_with_gender = pd.DataFrame(dataframe_maker)
print(issue_authors_with_gender)
issue_authors_with_gender.to_csv('issue_authors_with_gender.csv', index=False)

for index, row in comment_authors_df.iterrows():
    issue_id = row["issue_id"]
    comment_id = row["comment_id"]
    user_id = row["user_id"]
    login = row["login"]

    name = "" if pd.isna(row["name"]) else str(row["name"])
    location = "" if pd.isna(row["location"]) else str(row["location"])

    try:
        gender = gc.resolveGender(name, location)
        if not gender:
            gender = "unknown"
    except Exception:
        gender = "unknown"

    dataframe_maker_two["issue_id"].append(issue_id)
    dataframe_maker_two["comment_id"].append(comment_id)
    dataframe_maker_two["user_id"].append(user_id)
    dataframe_maker_two["login"].append(login)
    dataframe_maker_two["name"].append(name)
    dataframe_maker_two["location"].append(location)
    dataframe_maker_two["gender"].append(gender)

comments_with_gender = pd.DataFrame(dataframe_maker_two)
print(comments_with_gender.head())
comments_with_gender.to_csv("comments_with_gender.csv", index=False)