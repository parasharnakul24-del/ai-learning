"""
vertex_first_call.py
Week 1, Saturday — First Vertex AI call
"""

import vertexai
from vertexai.generative_models import GenerativeModel

# Your GCP project details
PROJECT_ID = "stone-nuance-456606-g9"
LOCATION = "us-central1"

# Initialise Vertex AI with your project and region
vertexai.init(project=PROJECT_ID, location=LOCATION)

# ── First call: Gemini 2.0 Flash ──────────────────────────────────
print("=" * 60)
print("First Vertex AI call — Gemini 2.0 Flash")
print("=" * 60)

model = GenerativeModel("gemini-2.5-flash")

response = model.generate_content(
    "In 3 bullet points, what are the main benefits of RAG "
    "(Retrieval Augmented Generation) for enterprise AI?"
)

print(response.text)
print("\nFirst Vertex AI call complete.")