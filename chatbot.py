import anthropic
from dotenv import load_dotenv
load_dotenv()

client = anthropic.Anthropic()

messages = []

while True:
    user_input = input('You: ')
    messages.append({'role': 'user', 'content': user_input})

    with client.messages.stream(
        model='claude-sonnet-4-6',
        max_tokens=512,
        system='You are a helpful AI tutor.',
        messages=messages
    ) as stream:
        reply = ''
        print('Claude: ', end='', flush=True)
        for text in stream.text_stream:
            print(text, end='', flush=True)
            reply += text
        print()
        messages.append({'role': 'assistant', 'content': reply})
