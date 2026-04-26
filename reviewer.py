from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a senior software engineer performing a code review.
Analyse the following git diff and provide clear, structured feedback.

Format your response exactly like this:

### Bugs
- List any bugs or potential errors (with line references if possible)
- If none, write: No bugs found.

### Security
- List any security vulnerabilities
- If none, write: No security issues found.

### Code Style
- List readability or naming issues
- If none, write: Looks clean.

### Performance
- List any performance concerns
- If none, write: No performance issues.

### Suggestions
- List any improvements or best practices to apply

Be specific and concise. Reference filenames and line numbers where possible.
"""

def review_code(diff_text):
    if not diff_text.strip():
        return "No code changes found to review."

    if len(diff_text) > 30000:
        diff_text = diff_text[:30000] + "\n\n[Diff truncated — too large]"

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": f"Code diff to review:\n\n{diff_text}"}
            ],
            max_tokens=1000
        )
        return response.choices[0].message.content

    except Exception as e:
        print(f"Groq API error: {e}")
        return f"AI review failed: {str(e)}"