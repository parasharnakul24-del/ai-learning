import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

MODEL = "claude-sonnet-4-6"

print("=" * 60)
print("MESSAGE PREFILLING — Modern Equivalent Patterns")
print("(Prefilling not supported on Claude 4.x models)")
print("=" * 60)
print()

# ── TEST 1: Without format control ─────────────────────────────
print("=== TEST 1: No format control (free-form response) ===")

response_plain = client.messages.create(
    model=MODEL,
    max_tokens=300,
    messages=[
        {
            "role": "user",
            "content": (
                "Extract the company name and founding year from this text: "
                "Acme Corp was founded in 1987 and is headquartered in New York."
            )
        }
    ]
)

print(response_plain.content[0].text)
print()

# ── TEST 2: System prompt for JSON-only output ──────────────────
print("=== TEST 2: System prompt enforces JSON (no preamble) ===")

response_json = client.messages.create(
    model=MODEL,
    max_tokens=300,
    system=(
        "You are a data extraction engine. "
        "Always respond with raw JSON only — no preamble, no explanation, no markdown fences. "
        "Output format: {\"company\": \"...\", \"founding_year\": ...}"
    ),
    messages=[
        {
            "role": "user",
            "content": (
                "Extract the company name and founding year from this text: "
                "Acme Corp was founded in 1987 and is headquartered in New York."
            )
        }
    ]
)

print(response_json.content[0].text)
print()

# ── TEST 3: Explicit schema in user message ─────────────────────
print("=== TEST 3: Schema in user message (inline instruction) ===")

response_schema = client.messages.create(
    model=MODEL,
    max_tokens=300,
    messages=[
        {
            "role": "user",
            "content": (
                "Extract data from the following text and return ONLY a JSON object "
                "with keys: company (string), founding_year (integer). "
                "No explanation. No markdown.\n\n"
                "Text: Acme Corp was founded in 1987 and is headquartered in New York."
            )
        }
    ]
)

print(response_schema.content[0].text)
print()

# ── TEST 4: Forced yes/no format via instruction ────────────────
print("=== TEST 4: Forced format — yes/no answer only ===")

response_yesno = client.messages.create(
    model=MODEL,
    max_tokens=50,
    system="Answer every question with a single word: Yes or No. Nothing else.",
    messages=[
        {
            "role": "user",
            "content": "Is Python a good language for AI development?"
        }
    ]
)

print(response_yesno.content[0].text)
print()

# ── TEST 5: Persona / tone control via system prompt ───────────
print("=== TEST 5: Persona control (what prefilling was used for) ===")

response_persona = client.messages.create(
    model=MODEL,
    max_tokens=200,
    system=(
        "You are a senior Salesforce Solution Engineer with deep AI expertise. "
        "Always start your response with: 'From an enterprise architecture perspective,'"
    ),
    messages=[
        {
            "role": "user",
            "content": "What is the best way to integrate AI into a CRM workflow?"
        }
    ]
)

print(response_persona.content[0].text)
print()

print("=" * 60)
print("KEY LEARNING:")
print("Claude 4.x dropped prefilling support.")
print("Modern equivalent = system prompt + explicit schema in user message.")
print("For SE interviews: 'How do you enforce output format on Claude?'")
print("Answer: system prompt with schema, not prefilling.")
print("=" * 60)