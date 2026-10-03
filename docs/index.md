---
title: PocketLLM Server
---

# PocketLLM Server

**Turn your iPhone into a private AI server.**

PocketLLM Server runs language models directly on your iPhone and makes them
available to your computers, apps and AI agents through an OpenAI-compatible
API on your local network. The iPhone runs the model; your computer runs your
code, tools and agents.

```
Laptop / Agent / App
          |
     OpenAI API  (Wi-Fi)
          v
       iPhone  ->  Local LLM
```

## Quick start

1. In PocketLLM, open **Models** and download a recommended model (or tap **+**
   to import your own GGUF file from Files).
2. Tap **Load**.
3. On the **Server** tab, tap **Start Server**.
4. Copy the **Endpoint** (`http://<iphone-ip>:8080/v1`) and the **API key**.
5. From a computer on the same Wi-Fi, point any OpenAI-compatible client at
   that endpoint.

```python
from openai import OpenAI

client = OpenAI(base_url="http://IPHONE_IP:8080/v1", api_key="YOUR_API_KEY")
reply = client.chat.completions.create(
    model="local-model",
    messages=[{"role": "user", "content": "Say hello in one short sentence."}],
)
print(reply.choices[0].message.content)
```

The app's **Connection Examples** screen gives you this snippet (and
PowerShell, curl and JavaScript versions) already filled in with your
endpoint and key.

## More

- [Examples](https://github.com/renjithsmenon/pocketllm-examples): Python,
  JavaScript, PowerShell and curl, including a tool-calling round trip
- [API reference](api/)
- [Compatible models](models/)
- [Support](support/)
- [Privacy policy](privacy/)

PocketLLM runs only while the app is open in the foreground: iOS pauses the
server when the app is backgrounded or the phone locks.
