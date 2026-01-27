import requests;
import pandas as pd;
from sodapy import Socrata;

#Loads the Violence Reduction - Victims of Homicides and Non-Fatal Shootings Data Set from the City
client = Socrata("data.cityofchicago.org", None)
results = client.get("gumc-mgzr", limit = 5000)
results_df = pd.DataFrame.from_records(results)

results_df["date"] = pd.to_datetime(results_df["date"])

results_df = results_df[results_df["date"].dt.year == 2026]

results_df = results_df[['date', 'victimization_primary',
                         'incident_primary', 'gunshot_injury_i',
                         'community_area', 'age', 'sex', 'race',
                         'location_description', 'latitude', 'longitude']]


from github import Github, InputGitTreeElement
import base64

# --- Configuration ---
# Your GitHub Personal Access Token (PAT)
GITHUB_TOKEN = "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" 
# Your GitHub username and the repository name
REPO_NAME = "audrey-ruh/VRDashboardData" 
# The path and filename for the new file in the GitHub repository
FILE_PATH = "2026_shooting_data.csv" 
# Commit message
COMMIT_MESSAGE = "Add new CSV data via Python API"
# Branch name (e.g., 'main' or 'master')
BRANCH = "main" # Change if your default branch is named differently

# Use df.to_csv(index=False) to get the string content
csv_content = results_df.to_csv(index=False) 

# --- 2. Authenticate and Access Repository ---
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

# --- 3. Check if file exists to get its SHA (required for updates) ---
file_sha = None
try:
    # Get the file contents and its SHA if it already exists
    contents = repo.get_contents(FILE_PATH, ref=BRANCH)
    file_sha = contents.sha
except Exception:
    # File doesn't exist, file_sha remains None
    pass

# --- 4. Create or Update the file ---
if file_sha:
    # Update existing file
    repo.update_file(FILE_PATH, COMMIT_MESSAGE, csv_content, file_sha, branch=BRANCH)
    print(f"File '{FILE_PATH}' updated successfully.")
else:
    # Create new file
    repo.create_file(FILE_PATH, COMMIT_MESSAGE, csv_content, branch=BRANCH)
    print(f"File '{FILE_PATH}' created successfully.")

# Close connection
g.close()


