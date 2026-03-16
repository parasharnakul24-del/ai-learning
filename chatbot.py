import anthropic
from dotenv import load_dotenv
load_dotenv()

client = anthropic.Anthropic()

messages = []
while True:
    user_input = input('You: ')
    messages.append({'role': 'user', 'content': user_input})
    response = client.messages.create(
        model='claude-sonnet-4-6',
        max_tokens=512,
        system='You are a helpful AI tutor.',
        messages=messages
    )
    reply = response.content[0].text
    messages.append({'role': 'assistant', 'content': reply})
    print('Claude:', reply)