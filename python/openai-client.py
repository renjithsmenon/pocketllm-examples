# Streaming chat against PocketLLM Server.
#   pip install openai
#   python openai-client.py

from openai import OpenAI

client = OpenAI(
    base_url="http://IPHONE_IP:8080/v1",
    api_key="YOUR_API_KEY",
)

stream = client.chat.completions.create(
    model="local-model",
    messages=[{"role": "user", "content": "Say hello in one short sentence."}],
    stream=True,
)
for chunk in stream:
    if chunk.choices and chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
print()
