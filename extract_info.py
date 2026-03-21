import anthropic
import json
from dotenv import load_dotenv
load_dotenv()

client = anthropic.Anthropic()

def extract_info(text):
    prompt = f"""Extract the following fields from the text below.
Return ONLY valid JSON with exactly these keys: name, company, email, role.
If a field is not found, use null.

<text>
{text}
</text>

Return ONLY the JSON, no other text. Do not wrap in markdown code blocks."""

    try:
        response = client.messages.create(
            model='claude-sonnet-4-6',
            max_tokens=256,
            messages=[{'role': 'user', 'content': prompt}]
        )
        raw = response.content[0].text
        # Strip markdown code blocks if present
        clean = raw.replace("```json", "").replace("```", "").strip()
        result = json.loads(clean)
        return result

    except json.JSONDecodeError:
        print("Claude returned invalid JSON — retrying...")
        print("Raw response was:", raw)
        return None

test_text = """
Hi, my name is Nakul Parashar and I work at Salesforce as a Solutions Engineer.
You can reach me at nakul@salesforce.com for any queries.
"""

result = extract_info(test_text)
print(json.dumps(result, indent=2))