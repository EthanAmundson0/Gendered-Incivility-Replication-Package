# Gendered-Incivility-Replication-Package
## Overview
This replication package contains all scripts and datasets necessary to reproduce the results from our study. Follow the steps below in order. Ensure that required input files and API tokens are configured correctly. All scripts should be run from the directory in which they and their associated input files reside.

## Project Structure
This project contains the following folders and files:
- **/datasets**: This folder contains all the datasets (xlsx/csv) which are needed to run the scripts, as well as the final enhanced datasets
- **/scripts**: This folder contains all the scripts needed to replicate our data enchancement/analysis

## Replication Steps
The following walks you through how to replicate the data from our study. Scripts and data files are in their respective folders.

### 1. Scan Issue Authors
1. Open the `issue_author_scanner.py` script and insert your personal GitHub token in the TOKEN field.
2. Ensure `issue_threads.csv` is located in the same folder as the script. This file can be accessed from the original GitHub repo, or in this package.
3. Run `issue_author_scanner.py`.
4. The script will output `issue_authors.csv`.

### 2. Scan Comment Authors
1. Open the `comment_author_scanner.py` script and add your GitHub token to the TOKEN field.
2. Ensure `comments.csv` is in the same folder as the script. This file can be accessed from the original GitHub repo, or in this package.
3. Run `comment_author_scanner.py`.
4. The script will output `comment_authors.csv`.

### 3. Gender Prediction
1. Place both `issue_authors.csv` and `comment_authors.csv` from the previous steps in the same folder as `gender_scanner.py`.
2. Run `gender_scanner.py`.
3. The script will generate two new files:
- `issue_authors_with_gender.csv`
- `comments_with_gender.csv`

### 4. Manual Gender Cleaning
**NOTE:** The genderComputer tool used in the previous steps script leaves some users marked as unknown or blank. These entries were manually reviewed.
1. Filter both generated datasets (`issue_authors_with_gender.csv`, `comments_with_gender.csv`) to identify unknown genders.
2. Review each GitHub user profile and annotate gender manually.
3. This package includes the following files which show our results after manual annotation:
- `issue_authors_with_gender_CLEANED.xlsx`
- `comments_with_gender_CLEANED.xlsx`

### 5. Issue Author & Commenter Join
1. Ensure both `issue_authors_with_gender_CLEANED.xlsx` and `comments_with_gender_CLEANED.xlsx` are in the same folder as the `gender_combine.py` script.
2. Run `gender_combine.py`.
> This will join the two tables together on 'issue_id' with a left join, so each comment entry will map to one issue, and one issue will have multiple comments. The script then filters the data frame so only genders in (male, female, unisex) are included. Finally it adds three columns representing if the comment was from a male to a female, male to unisex, or male to minority.
3. The script will output `comments_with_author_gender_flags_filtered.xlsx`.

### 6. Incivility Annotation Join
1. Ensure both `comments_with_author_gender_flags_filtered.xlsx` and `annotated_comment_level.csv` are in the same folder as the `annotated_join.py` script.
2. `annotated_comment_level.csv` can be accessed from the original GitHub repo, or in this package.
3. Run `annotated_join.py`.
> The script adds the incivility annotation (tbdf) to each comment.
4. The output will be `comments_with_gender_and_tbdf.xlsx` which is the final file we used for our analysis.
