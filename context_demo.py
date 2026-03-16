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
        "content": f"Here is a product description:\n\n{product_info}\n\nIn 3 bullet points, what are the top selling points of this product?"
    }]
)

print(message.content[0].text)