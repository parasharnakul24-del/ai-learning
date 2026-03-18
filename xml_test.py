import anthropic
from dotenv import load_dotenv
load_dotenv()

client = anthropic.Anthropic()

document_text = """
FlowSync is a real-time data integration platform.
It supports 200+ connectors including Salesforce and SAP.
Pricing starts at $499 per month.
It is SOC 2 Type II compliant.
"""

# WITHOUT XML tags
prompt_without = f"Summarise this document: {document_text}"

# WITH XML tags
prompt_with = f"""Summarise the document below in 2 sentences.

<document>
{document_text}
</document>

Return your summary inside <summary> tags."""

# Test both
for label, prompt in [("WITHOUT XML", prompt_without), ("WITH XML", prompt_with)]:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )
    print(f"\n--- {label} ---")
    print(response.content[0].text)
