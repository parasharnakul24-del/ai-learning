"""
prompts_library.py
Week 1, Day 5 — 5 reusable prompt templates with XML tags + prompt caching

Prompts:
1. customer_service_agent    — responds to customer issues professionally
2. document_analyser         — extracts key points, sentiment, action items
3. code_reviewer             — bugs, security, improvements, revised code
4. data_extractor            — pulls structured fields from unstructured text
5. executive_summary_writer  — boardroom-ready summary calibrated to audience
"""

import anthropic
import json
import re

client = anthropic.Anthropic()

# ── Cached system prompt ──────────────────────────────────────────────────────
# Must be 1024+ tokens to qualify for caching.
# Written to cache on first call (~25% extra cost), read at 90% discount after.

SYSTEM_PROMPT = """
You are an expert AI assistant helping a Salesforce Solutions Engineer
transition into an AI company SE role. You produce clean, structured,
professional output. You always follow the XML tags provided in each
prompt exactly — no deviations.

Rules you always follow:
- Respond only with content inside the requested XML tags
- Never add preamble like "Sure!" or "Here you go!"
- Keep responses concise and actionable
- Use plain English — no unnecessary jargon
- When asked for bullet points, use the bullet character
- When asked for code, wrap it in triple backticks with the language name
- When asked for structured data, return valid JSON only
- Always complete the full response — never truncate
- When a field is missing and strict mode is true, return null
- When given a word limit, never exceed it

You have deep expertise in:
- Large language models and transformer architecture
- Claude API, Anthropic products, and AI safety
- Salesforce platform, Data Cloud, Agentforce, and CRM AI features
- Python development, REST APIs, and cloud deployment (GCP, AWS)
- Solutions engineering, technical pre-sales, and enterprise AI adoption
- Prompt engineering, RAG, LangChain, LangGraph, and agentic systems
- Model Context Protocol (MCP) and Claude Agent SDK
- AI evaluation, observability, and production deployment patterns

When calibrating tone to audience:
- C-suite    → revenue impact, risk, strategic fit — no technical detail
- board      → governance, fiduciary risk, long-term outlook
- investor   → ROI, market opportunity, competitive moat
- tech-lead  → architecture decisions, tradeoffs, implementation risk
- sales-mgr  → pipeline impact, customer value prop, competitive positioning

When reviewing code, you think like a senior engineer:
- Separate what is broken, what is risky, what could be better
- Always provide a revised version, not just commentary
- Flag security issues even when focus is set to style or performance

When extracting data:
- In strict mode, never guess — return null for anything not explicitly stated
- In non-strict mode, make reasonable inferences but flag them

You are concise, direct, and always helpful. Every response adds value.
""".strip()


# ── Core API call with prompt caching ────────────────────────────────────────

def call_claude(user_prompt: str) -> str:
    """
    Calls Claude with the cached system prompt.
    First call: writes system prompt to cache (cache_creation_input_tokens > 0)
    Subsequent calls: reads from cache at 90% less cost (cache_read_input_tokens > 0)
    Cache TTL: 5 minutes, resets on each read.
    """
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"}
            }
        ],
        messages=[{"role": "user", "content": user_prompt}]
    )

    usage = response.usage
    if hasattr(usage, 'cache_read_input_tokens') and usage.cache_read_input_tokens:
        print(f"  [cache] hit  — {usage.cache_read_input_tokens} tokens read from cache")
    if hasattr(usage, 'cache_creation_input_tokens') and usage.cache_creation_input_tokens:
        print(f"  [cache] miss — {usage.cache_creation_input_tokens} tokens written to cache")

    return response.content[0].text


def extract_tag(text: str, tag: str) -> str:
    """Extract content between <tag> and </tag>."""
    match = re.search(rf"<{tag}>(.*?)</{tag}>", text, re.DOTALL)
    return match.group(1).strip() if match else text.strip()


# ══════════════════════════════════════════════════════════════════════════════
# PROMPT 1 — Customer Service Agent
# ══════════════════════════════════════════════════════════════════════════════

def customer_service_agent(customer_name: str, issue: str,
                            order_id: str = None) -> str:
    """
    Responds to a customer issue with empathy and a clear next step.
    XML tags: <customer_name>, <issue>, <order_id>, <response>
    """
    prompt = f"""
You are a professional customer service agent. Respond to the customer's
issue with empathy, clarity, and a clear next step.

<customer_name>{customer_name}</customer_name>
<issue>{issue}</issue>
<order_id>{order_id if order_id else "not provided"}</order_id>

Return your response in this exact format:
<response>
your reply to the customer here
</response>
""".strip()

    result = call_claude(prompt)
    return extract_tag(result, "response")


# ══════════════════════════════════════════════════════════════════════════════
# PROMPT 2 — Document Analyser
# ══════════════════════════════════════════════════════════════════════════════

def document_analyser(document: str,
                       analysis_type: str = "general") -> str:
    """
    Analyses any document and returns key points, sentiment, action items.
    XML tags: <document>, <analysis_type>, <key_points>, <sentiment>, <action_items>
    analysis_type options: "general" | "legal" | "financial" | "technical" | "sales"
    """
    prompt = f"""
Analyse the document below thoroughly.
Calibrate your analysis to the specified type.

<analysis_type>{analysis_type}</analysis_type>

<document>
{document}
</document>

Return your response in this exact format:
<key_points>
* point 1
* point 2
* point 3
</key_points>

<sentiment>positive | neutral | negative — one word then one sentence explanation</sentiment>

<action_items>
* action 1
* action 2
</action_items>
""".strip()

    return call_claude(prompt)


# ══════════════════════════════════════════════════════════════════════════════
# PROMPT 3 — Code Reviewer
# ══════════════════════════════════════════════════════════════════════════════

def code_reviewer(code: str, language: str = "python",
                  focus: str = "all") -> str:
    """
    Reviews code for bugs, security risks, and improvements.
    Returns issues and a revised version.
    XML tags: <code>, <language>, <focus>, <bugs>, <security>, <improvements>, <revised_code>
    focus options: "all" | "bugs" | "security" | "performance" | "style"
    """
    prompt = f"""
Review the following code carefully and thoroughly.

<language>{language}</language>
<focus>{focus}</focus>

<code>
{code}
</code>

Return your response in this exact format:
<bugs>
* bug — explanation
(or "None found" if clean)
</bugs>

<security>
* risk — explanation
(or "None found" if clean)
</security>

<improvements>
* improvement 1
* improvement 2
</improvements>

<revised_code>
```{language}
revised code here
```
</revised_code>
""".strip()

    return call_claude(prompt)


# ══════════════════════════════════════════════════════════════════════════════
# PROMPT 4 — Data Extractor
# ══════════════════════════════════════════════════════════════════════════════

def data_extractor(text: str, fields: list,
                   strict: bool = False) -> dict:
    """
    Pulls structured fields from any unstructured text. Returns a Python dict.
    XML tags: <text>, <fields>, <strict_mode>, <extracted_data>
    strict=True  — returns null for missing fields, never guesses
    strict=False — makes reasonable inferences, flags inferred values
    """
    fields_formatted = "\n".join(f"  - {f}" for f in fields)
    strict_instruction = (
        "true — only extract what is explicitly stated. Use null for anything not found."
        if strict else
        "false — use reasonable inference for missing fields but flag inferred values with (inferred)."
    )

    prompt = f"""
Extract the specified fields from the unstructured text below.

<strict_mode>{strict_instruction}</strict_mode>

<fields>
{fields_formatted}
</fields>

<text>
{text}
</text>

Return ONLY a valid JSON object inside these tags — no explanation, no preamble:
<extracted_data>
JSONHERE
</extracted_data>
""".strip()

    result = call_claude(prompt)
    raw = extract_tag(result, "extracted_data")
    try:
        return json.loads(raw.strip())
    except json.JSONDecodeError:
        return {"error": "JSON parse failed", "raw": raw}


# ══════════════════════════════════════════════════════════════════════════════
# PROMPT 5 — Executive Summary Writer
# ══════════════════════════════════════════════════════════════════════════════

def executive_summary_writer(content: str, audience: str = "C-suite",
                              max_words: int = 150) -> str:
    """
    Condenses any content into a boardroom-ready summary.
    XML tags: <content>, <audience>, <max_words>, <headline>, <summary>, <recommendation>
    audience options: "C-suite" | "board" | "investor" | "technical-lead" | "sales-manager"
    """
    prompt = f"""
Write an executive summary of the content below.
Calibrate tone, vocabulary and focus to the specified audience.

<audience>{audience}</audience>
<max_words>{max_words}</max_words>

<content>
{content}
</content>

Return your response in this exact format:

<headline>
one punchy sentence that captures the single most important point
</headline>

<summary>
the full executive summary — max {max_words} words, no bullet points,
written in plain business English for the specified audience
</summary>

<recommendation>
one clear recommended action, starting with a verb
</recommendation>
""".strip()

    return call_claude(prompt)


# ══════════════════════════════════════════════════════════════════════════════
# DEMO — runs all 5 prompts
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":

    SEP = "=" * 60

    # 1. Customer Service Agent
    print(SEP)
    print("PROMPT 1 — Customer Service Agent")
    print(SEP)
    print(customer_service_agent(
        customer_name="Priya Singh",
        issue="My order arrived damaged and I need a replacement urgently.",
        order_id="ORD-20394"
    ))

    # 2. Document Analyser
    print(f"\n{SEP}")
    print("PROMPT 2 — Document Analyser")
    print(SEP)
    doc = """
    Q3 2026 results show revenue up 34% YoY driven by enterprise AI contracts.
    Operating costs increased 18% due to GPU infrastructure investment.
    Customer churn dropped to 3.2%, the lowest in company history.
    The board has approved a $50M expansion into the APAC market for Q1 2027.
    Key risk: regulatory uncertainty around AI governance in the EU may delay
    the planned product launch in Germany and France.
    """
    print(document_analyser(doc, analysis_type="financial"))

    # 3. Code Reviewer
    print(f"\n{SEP}")
    print("PROMPT 3 — Code Reviewer")
    print(SEP)
    code = """
def get_user(id):
    import requests
    r = requests.get("https://api.example.com/users/" + id)
    data = r.json()
    return data['name']
    """
    print(code_reviewer(code, language="python", focus="security"))

    # 4. Data Extractor
    print(f"\n{SEP}")
    print("PROMPT 4 — Data Extractor")
    print(SEP)
    raw_text = """
    Had a great call with Rahul Mehta, CTO at FinanceAI Ltd in Mumbai.
    They are looking to deploy an LLM solution by end of Q1 2027.
    Budget is around $120k. Rahul's email is rahul.m@financeai.com.
    Main pain point is manual document processing taking 3 days per report.
    """
    extracted = data_extractor(
        raw_text,
        fields=["name", "title", "company", "email", "budget", "timeline", "pain_point"],
        strict=False
    )
    print(json.dumps(extracted, indent=2))

    # 5. Executive Summary Writer
    print(f"\n{SEP}")
    print("PROMPT 5 — Executive Summary Writer")
    print(SEP)
    report = """
    Our AI pilot with 3 enterprise clients over 90 days showed a 41% reduction
    in document processing time and a 28% drop in operational costs. NPS scores
    improved from 32 to 67. All 3 clients have indicated intent to expand.
    Implementation took an average of 6 weeks. Support tickets dropped 22%.
    Estimated annual value per client: $400k in productivity gains.
    """
    print(executive_summary_writer(report, audience="C-suite", max_words=120))

    print(f"\n{SEP}")
    print("All 5 prompts complete.")
    print(SEP)
