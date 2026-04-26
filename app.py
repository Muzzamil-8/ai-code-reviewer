# It's a Main server. It receives Github webhooks, run the review and post comments
import hmac
import hashlib
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

from github_client import get_pr_files, extract_diff, post_pr_comment
from reviewer import review_code

load_dotenv()

app = Flask(__name__)

GITHUB_TOKEN  = os.getenv("GITHUB_TOKEN")
GITHUB_OWNER  = os.getenv("GITHUB_OWNER")
GITHUB_REPO   = os.getenv("GITHUB_REPO")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")


def verify_signature(payload_body, signature_header):
    """Verify the request really came from GitHub."""
    if not WEBHOOK_SECRET:
        return True  # skip verification in development
    if not signature_header:
        return False
    expected = "sha256=" + hmac.new(
        WEBHOOK_SECRET.encode(),
        payload_body,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature_header)


@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "AI Code Reviewer is running"})


@app.route("/webhook", methods=["POST"])
def webhook():
    # Step 1 — Verify the request is from GitHub
    signature = request.headers.get("X-Hub-Signature-256")
    if not verify_signature(request.get_data(), signature):
        return jsonify({"error": "Unauthorized"}), 401

    # Step 2 — Only handle pull_request events
    event = request.headers.get("X-GitHub-Event")
    if event != "pull_request":
        return jsonify({"message": "Not a PR event, ignoring"}), 200

    data = request.json
    action = data.get("action")

    # Step 3 — Only review when PR is opened or new commits pushed
    if action not in ["opened", "synchronize"]:
        return jsonify({"message": f"Action '{action}' ignored"}), 200

    # Step 4 — Extract PR details
    pr_number = data["pull_request"]["number"]
    pr_title  = data["pull_request"]["title"]
    owner     = data["repository"]["owner"]["login"]
    repo      = data["repository"]["name"]

    print(f"Reviewing PR #{pr_number}: {pr_title}")

    # Step 5 — Fetch changed files from GitHub
    files = get_pr_files(owner, repo, pr_number)
    if not files:
        return jsonify({"message": "No files to review"}), 200

    # Step 6 — Extract the diff text
    diff = extract_diff(files)
    if not diff.strip():
        return jsonify({"message": "No reviewable diff found"}), 200

    # Step 7 — Send to Gemini for review
    print("Sending diff to Gemini...")
    review = review_code(diff)

    # Step 8 — Post review back to GitHub PR
    print("Posting review comment...")
    success = post_pr_comment(owner, repo, pr_number, review)

    if success:
        return jsonify({"message": "Review posted successfully"}), 200
    else:
        return jsonify({"error": "Failed to post review"}), 500


if __name__ == "__main__":
    print("Starting AI Code Reviewer...")
    print(f"Owner: {GITHUB_OWNER} | Repo: {GITHUB_REPO}")
    app.run(host="0.0.0.0", port=5000, debug=True)