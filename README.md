# AI Code Review Assistant

Automatically reviews GitHub Pull Requests using Groq (Llama 3) AI.
Posts structured feedback as PR comments covering bugs, security,
style, performance, and suggestions.

## Live Demo
Deployed at: https://ai-code-reviewer.onrender.com

## Tech Stack
Python · Flask · Groq (Llama 3) · GitHub API · Render

## How It Works
1. Developer opens a PR on GitHub
2. GitHub sends a webhook to this server
3. Server fetches the changed code via GitHub API
4. Code diff is sent to Llama 3 (via Groq) for review
5. AI feedback is posted as a PR comment automatically

## Setup (run your own instance)

1. Clone the repo
   git clone https://github.com/Muzzamil-8/ai-code-reviewer

2. Install dependencies
   pip install -r requirements.txt

3. Add your keys to .env
   GITHUB_TOKEN=your_github_token
   GROQ_API_KEY=your_groq_key
   GITHUB_OWNER=your_github_username
   GITHUB_REPO=your_repo_name

4. Run the server
   python app.py

5. Add webhook URL to your GitHub repo
   Settings → Webhooks → Add webhook
   URL: https://your-render-url.onrender.com/webhook
   Events: Pull requests only

## Sample Review Output

### Bugs
- Line 13: `if user == None` should be `if user is None`

### Security
- Line 14: SQL injection vulnerability — use parameterised queries

### Code Style
- Variable name `x` is not descriptive — use `user_record`

### Performance
- No performance issues found.

### Suggestions
- Add input validation before database calls
- Consider using an ORM for database interactions
