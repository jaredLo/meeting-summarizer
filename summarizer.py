import os
import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
VAULT   = os.getenv("VAULT_PATH")
NOTE    = os.getenv("NOTE_NAME")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)

current_summary = ""
buffered = []

def update_summary(new_text):
    """
    Buffer incoming text; once we have enough, call the LLM to get an updated
    summary. If it differs from our last summary, append it as a new paragraph
    (with timestamp) in the Obsidian note.
    """
    global current_summary, buffered

    buffered.append(new_text)
    if len(buffered) < 2:           # throttle to ~10s or 2 chunks
        return

    recent = "\n".join(buffered[-3:])
    prompt = (
        f"Previous summary:\n{current_summary or '[none]'}\n\n"
        f"Update the summary with this new dialogue (highlight topic shifts):\n"
        f"{recent}"
    )

    resp = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You’re a ruthless summarizer."},
            {"role": "user",   "content": prompt}
        ],
        timeout=15,
    )
    new_summary = resp.choices[0].message.content.strip()
    buffered.clear()

    # If nothing changed, bail out
    if not new_summary or new_summary == current_summary:
        return

    current_summary = new_summary
    append_paragraph(new_summary)

def append_paragraph(text: str):
    """
    Append a new paragraph (the text) to the markdown note, followed by
    a timestamp on its own line.
    """
    path = os.path.join(VAULT, NOTE)
    # Ensure file exists with a top-level header
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write("# Live Meeting Summary\n\n")

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(path, "a") as f:
        f.write(f"---\n\n{text}\n\n*Updated: {timestamp}*\n\n")