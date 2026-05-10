import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

# ── TWO-MODEL ARCHITECTURE ───────────────────────────────────────
# Haiku classifies intent (fast, cheap)
# Sonnet handles complex responses (quality)

HAIKU  = "claude-haiku-4-5-20251001"
SONNET = "claude-sonnet-4-6"

SIMPLE_INTENTS = ["greeting", "simple_question", "yes_no", "classification"]
COMPLEX_INTENTS = ["analysis", "coding", "document", "agent_task", "strategic"]

def classify_intent(user_message):
    """Use Haiku to classify — costs almost nothing."""
    response = client.messages.create(
        model=HAIKU,
        max_tokens=20,
        system=(
            "Classify the user message into exactly one category: "
            "greeting, simple_question, yes_no, classification, "
            "analysis, coding, document, agent_task, strategic. "
            "Reply with the category name only. No explanation."
        ),
        messages=[{"role": "user", "content": user_message}]
    )
    return response.content[0].text.strip().lower()


def smart_respond(user_message):
    """Route to cheapest model that can handle the task."""
    intent = classify_intent(user_message)
    print(f"  Intent: {intent}")

    if intent in SIMPLE_INTENTS:
        model = HAIKU
        print(f"  Routed to: Haiku (simple)")
    else:
        model = SONNET
        print(f"  Routed to: Sonnet (complex)")

    response = client.messages.create(
        model=model,
        max_tokens=500,
        messages=[{"role": "user", "content": user_message}]
    )

    return response.content[0].text, model


# ── TEST CASES ───────────────────────────────────────────────────
queries = [
    "Hi there!",
    "Is Python good for AI?",
    "Analyse the build vs buy trade-offs for an enterprise AI platform",
    "Write a Python function to parse JSON with error handling",
    "What is 2 + 2?",
]

print("=" * 60)
print("TWO-MODEL ROUTING DEMO")
print("=" * 60)

for query in queries:
    print(f"\nQ: {query}")
    answer, model_used = smart_respond(query)
    print(f"A: {answer[:150]}...")
    print(f"  Model used: {model_used}")

print("\n" + "=" * 60)
print("KEY LEARNING:")
print("Haiku → greetings, yes/no, classification (~$0.000001/call)")
print("Sonnet → analysis, coding, agents (~$0.000015/call)")
print("Routing saves ~60% cost on mixed-intent production traffic")
print("=" * 60)