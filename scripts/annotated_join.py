import pandas as pd

comments_gender = pd.read_excel("comments_with_author_gender_Filtered.xlsx")
annotated = pd.read_csv("annotated_comment_level.csv", keep_default_na=False)

merged = comments_gender.merge(
    annotated[["comment_id", "tbdf"]],
    on="comment_id",
    how="left"
)

merged.to_excel("comments_with_gender_and_tbdf.xlsx", index=False)