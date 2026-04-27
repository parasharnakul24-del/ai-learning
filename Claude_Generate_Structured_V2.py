from dotenv import load_dotenv
load_dotenv()

import anthropic
client = anthropic.Anthropic()

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
Generate 3 different AWS CLI commands, each very short.
Return ONLY the commands, one per line, each wrapped in backticks.
End with the word DONE.
Example format:
`aws s3 ls`
`aws ec2 describe-instances`
`aws iam list-users`
DONE"""

add_user_message(messages, prompt)
text = chat(messages)

# Extract lines that are wrapped in backticks
commands = []
for line in text.splitlines():
    line = line.strip()
    if line.startswith("`") and line.endswith("`"):
        commands.append(line.strip("`"))
    if line == "DONE":
        break

for cmd in commands:
    print(cmd)