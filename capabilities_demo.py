import anthropic
import base64
import httpx
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

# --- Use a reliable test image (no auth/headers needed) ---
image_url = "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=400"
response = httpx.get(image_url, follow_redirects=True)

print(f"Status: {response.status_code}")
print(f"Size: {len(response.content)} bytes")

image_data = base64.standard_b64encode(response.content).decode("utf-8")

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=300,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": image_data
                }
            },
            {
                "type": "text",
                "text": "Describe this image in 2 sentences."
            }
        ]
    }]
)

print("\n=== Claude Vision Response ===")
print(message.content[0].text)
print(f"\nTokens used — Input: {message.usage.input_tokens} | Output: {message.usage.output_tokens}")

# --- Text-only Demo: Compare the API structure ---
message2 = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=300,
    messages=[{
        "role": "user",
        "content": "What are the 3 main types of biomes? One sentence each."
    }]
)

print("\n=== Claude Text Response ===")
print(message2.content[0].text)
print(f"\nTokens used — Input: {message2.usage.input_tokens} | Output: {message2.usage.output_tokens}")