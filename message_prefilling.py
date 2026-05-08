import anthropic
import json
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

# ── TEST 1: Without prefilling ──────────────────────────────────────────────
response_plain = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=300,
    messages=[
        {
            "role": "user",
            "content": "Extract the company name and founding year from this text: Acme Corp was founded in 1987 and is headquartered in New York."
        }
    ]
)
print("=== WITHOUT PREFILLING ===")
print(response_plain.content[0].text)
print()

response_modern = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=300,
    system="Always respond with raw JSON only. No preamble, no explanation.",
    messages=[
        {
            "role": "user",
            "content": "Extract company name and founding year: Acme Corp was founded in 1987."
        }
    ]
)