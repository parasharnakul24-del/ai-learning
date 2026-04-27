"""
model_comparison.py
Week 1, Saturday — Multi-model comparison
Gemini 2.5 Flash + Gemini 2.5 Flash-Lite (via Vertex) vs Claude Sonnet (via Anthropic API)
"""

import vertexai
from vertexai.generative_models import GenerativeModel
import anthropic
from dotenv import load_dotenv

load_dotenv()

# ── Setup ─────────────────────────────────────────────────────────
PROJECT_ID = "stone-nuance-456606-g9"
LOCATION = "us-central1"
vertexai.init(project=PROJECT_ID, location=LOCATION)

anthropic_client = anthropic.Anthropic()

# ── Same prompt sent to all 3 models ─────────────────────────────
PROMPT = """You are helping an enterprise sales team.
A customer asks: "Why should we choose your AI platform over building in-house?"
Give a concise, compelling 3-point answer."""

SEP = "=" * 60

# ── Model 1: Gemini 2.5 Flash (Vertex) ───────────────────────────
print(SEP)
print("MODEL 1 — Gemini 2.5 Flash (via Vertex AI)")
print(SEP)
flash = GenerativeModel("gemini-2.5-flash")
r1 = flash.generate_content(PROMPT)
print(r1.text)

# ── Model 2: Gemini 2.5 Flash-Lite (Vertex) ──────────────────────
print(f"\n{SEP}")
print("MODEL 2 — Gemini 2.5 Flash-Lite (via Vertex AI)")
print(SEP)
lite = GenerativeModel("gemini-2.5-flash-lite")
r2 = lite.generate_content(PROMPT)
print(r2.text)

# ── Model 3: Claude Sonnet 4.6 (Anthropic API) ───────────────────
print(f"\n{SEP}")
print("MODEL 3 — Claude Sonnet 4.6 (via Anthropic API)")
print(SEP)
r3 = anthropic_client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=512,
    messages=[{"role": "user", "content": PROMPT}]
)
print(r3.content[0].text)

# ── Summary ───────────────────────────────────────────────────────
print(f"\n{SEP}")
print("COMPARISON SUMMARY")
print(SEP)
print(f"{'Model':<30} {'Provider':<15} {'Access'}")
print("-" * 60)
print(f"{'Gemini 2.5 Flash':<30} {'Google':<15} {'Vertex AI (free trial)'}")
print(f"{'Gemini 2.5 Flash-Lite':<30} {'Google':<15} {'Vertex AI (free trial)'}")
print(f"{'Claude Sonnet 4.6':<30} {'Anthropic':<15} {'Direct API'}")
print(f"\nSame prompt — 3 different models. Note your observations.")
print(SEP)
