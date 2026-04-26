# AI Code Review Assistant

Automatically reviews GitHub Pull Requests using Google Gemini AI.
Posts structured feedback as PR comments covering bugs, security,
style, performance, and suggestions.

## Tech Stack
Python · Flask · GitHub API · Google Gemini 1.5 Flash

## Setup

1. Clone the repo
   git clone https://github.com/muzzamal-kosar/ai-code-reviewer

2. Install dependencies
   pip install -r requirements.txt

3. Add your keys to .env
   GITHUB_TOKEN=your_token
   GEMINI_API_KEY=your_key

4. Run the server
   python app.py

5. Expose locally with ngrok
   ngrok http 5000

6. Add webhook URL to your GitHub repo
   Settings → Webhooks → Add webhook
   URL: https://your-ngrok-url.ngrok.io/webhook
   Events: Pull requests

## How It Works
1. Developer opens a PR on GitHub
2. GitHub sends a webhook to this server
3. Server fetches the changed code via GitHub API
4. Code diff is sent to Gemini for review
5. AI feedback is posted as a PR comment automatically