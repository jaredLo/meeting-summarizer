import os, time, requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
VAULT = os.getenv("VAULT_PATH")
NOTE = os.getenv("NOTE_NAME")

summary = "Meeting kicked off. Stay tuned."
buffered = []

def update_summary(new_text):
    global summary, buffered
    buffered.append(new_text)
    if len(buffered) < 2:  # throttle to ~10s; adjust as needed
        return

    recent = "\n".join(buffered[-3:])
    prompt = (
      f"Current summary:\n{summary}\n\n"
      f"Update with this new dialogue (note topic shifts):\n{recent}"
    )
    resp = requests.post(
      "https://api.openai.com/v1/chat/completions",
      headers={"Authorization":f"Bearer {API_KEY}"},
      json={
        "model":"gpt-3.5-turbo",
        "messages":[
          {"role":"system","content":"You’re a ruthless summarizer."},
          {"role":"user","content":prompt}
        ]
      },
      timeout=15

    )
    summary = resp.json()["choices"][0]["message"]["content"].strip()
    buffered = []
    write_to_obsidian(summary)

def write_to_obsidian(text):
    path = os.path.join(VAULT, NOTE)
    with open(path, "w") as f:
        f.write(f"# Live Meeting Summary\n\n{text}\n\n*Updated: {time.strftime('%H:%M:%S')}*")