# Handles all communication with github
import requests
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}


def get_pr_files(owner, repo, pr_number):
    """Fetch all changed files in a PR."""
    url = (
        f"https://api.github.com/repos/"
        f"{owner}/{repo}/pulls/{pr_number}/files"
    )
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"GitHub API error: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching PR files: {e}")
        return []


def extract_diff(files):
    """Extract the code diff text from PR files."""
    diff_text = ""
    for file in files:
        # Skip deleted files
        if file["status"] == "removed":
            continue
        # Skip files with no patch (very large files)
        if "patch" not in file:
            continue

        diff_text += f"\n=== File: {file['filename']} ({file['status']}) ===\n"
        diff_text += f"Changes: +{file['additions']} additions, -{file['deletions']} deletions\n"
        diff_text += file["patch"]
        diff_text += "\n"

    return diff_text


def post_pr_comment(owner, repo, pr_number, review_text):
    """Post AI review as a comment on the PR."""
    comment_body = f"""## AI Code Review

{review_text}

---
*Automated review powered by Gemini AI*
"""

    url = (
        f"https://api.github.com/repos/"
        f"{owner}/{repo}/issues/{pr_number}/comments"
    )

    try:
        response = requests.post(
            url,
            headers=HEADERS,
            json={"body": comment_body},
            timeout=10
        )
        if response.status_code == 201:
            print(f"Successfully posted review on PR #{pr_number}")
            return True
        else:
            print(f"Failed to post comment: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"Exception posting comment: {e}")
        return False