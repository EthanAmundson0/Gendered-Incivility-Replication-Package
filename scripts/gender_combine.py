import pandas as pd

authors_df = pd.read_excel("issue_authors_with_gender_CLEANED.xlsx")
comments_df = pd.read_excel("comments_with_gender_CLEANED.xlsx")

merged = comments_df.merge(
    authors_df[["issue_id", "gender"]].rename(columns={"gender": "issue_author_gender"}),
    on="issue_id",
    how="left"
)

genders = ["male", "female", "unisex"]

filtered = merged[
    (merged["gender"].isin(genders)) & 
    (merged["issue_author_gender"].isin(genders))
].copy()

filtered["FromMaleToFemale"] = (
    (filtered["gender"] == "male") & (filtered["issue_author_gender"] == "female")
)

filtered["FromMaleToUnisex"] = (
    (filtered["gender"] == "male") & (filtered["issue_author_gender"] == "unisex")
)

filtered["FromMaleToUnisexOrFemale"] = (
    (filtered["gender"] == "male") & 
    (filtered["issue_author_gender"].isin(["female", "unisex"]))
)

filtered.to_excel("comments_with_author_gender_flags_filtered.xlsx", index=False)
