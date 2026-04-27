from dotenv import load_dotenv
load_dotenv()

import anthropic
client = anthropic.Anthropic()

# ── Helper functions ──────────────────────────────────────
def add_user_message(messages, text):
    messages.append({"role": "user", "content": text})

def chat(messages):
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=512,
        messages=messages
    )
    return response.content[0].text

# ── Main ──────────────────────────────────────────────────
messages = []

prompt = """
Generate 3 different AWS CLI commands, each should be very short."""

add_user_message(messages, prompt)

text = chat(messages)
print(text.strip())          # ← you need print() or the output won't show

