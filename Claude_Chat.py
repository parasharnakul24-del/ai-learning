
from dotenv import load_dotenv
load_dotenv()                    # ← this reads the .env file

import anthropic
client = anthropic.Anthropic()
import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env

def add_user_message(messages, text):
    messages.append({"role": "user", "content": text})

def add_assistant_message(messages, text):
    messages.append({"role": "assistant", "content": text})

def chat(messages, system =""):
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=512,
        system="You are a python engineer who writes very concise code ",
        messages=messages
    )
    return response.content[0].text


# --- Main loop ---
messages = []

while True:
    user_input = input("> ")
    print(">", user_input)

    add_user_message(messages, user_input)
    answer = chat(messages)

    add_assistant_message(messages, answer)

    print("---")
    print(answer)