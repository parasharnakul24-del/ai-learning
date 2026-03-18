import anthropic
from dotenv import load_dotenv
load_dotenv()

def read_file(path):
    with open(path, "r") as f:
        return f.read()

product_info = read_file("product.txt")
client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=300,
    messages=[{
        "role": "user",
        "content": (
            "<request>\n"
            "  <instruction>In 3 bullet points, what are the top selling points of this product?</instruction>\n"
            "  <productText>\n"
            f"{product_info}"
            "  </productText>\n"
            "</request>"
        )
    }]
)

print(message.content[0].text)git add context_demo.py xml_test.py