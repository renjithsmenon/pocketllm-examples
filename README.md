# Use your iPhone as a local LLM server

Small, working examples for **PocketLLM Server**, which turns an iPhone into
an OpenAI-compatible inference endpoint on your local network. The iPhone runs
the model. Your computer runs your code, agents and tools.

```
Laptop / Agent / App
          |
     OpenAI API  (Wi-Fi)
          v
       iPhone  ->  Local LLM
```

## Before you start

1. In PocketLLM, import a GGUF model, load it, and start the server.
2. On the Server tab, note the **Endpoint** (`http://<iphone-ip>:8080/v1`) and copy the **API key**.
3. Your computer must be on the same Wi-Fi network, and PocketLLM must stay open in the foreground.

In each example, replace `IPHONE_IP` and `YOUR_API_KEY`. `local-model` is
accepted as the model name and means "whatever is loaded"; the exact model ID
is listed at `/v1/models`.

## Examples

| Folder | What it shows |
|---|---|
| `python/openai-client.py` | Streaming chat with the official `openai` SDK |
| `python/tool_calling_test.py` | Health check, streaming, and a full tool-calling round trip (the tool runs on your computer) |
| `javascript/openai-client.mjs` | Streaming chat with the `openai` npm package |
| `powershell/chat.ps1` | One chat completion with `Invoke-RestMethod` |
| `powershell/test-pocketllm.ps1` | Health, models, auth check, buffered and streaming chat, metrics |
| `curl/examples.md` | Health, model list, streaming chat |

The OpenAI SDKs also read `OPENAI_BASE_URL` and `OPENAI_API_KEY`. The API Key
screen in the app has both, ready to copy.

## Troubleshooting

- **Connection refused or timeout:** confirm the server is running and PocketLLM is in the foreground. Check both devices are on the same network, and that the network doesn't isolate clients (guest Wi-Fi often does).
- **401:** the API key is wrong, or it was regenerated in the app.
- **503:** no model is loaded.
- **429:** a request is already generating. PocketLLM serves one at a time.
- **400 `tools_unsupported`:** the loaded model's chat template can't express tool calls. Load a tool-capable model.

## Help, privacy and docs

- **Support and troubleshooting:** https://renjithsmenon.github.io/pocketllm-examples/support/
- **Questions and bug reports:** [open an issue](https://github.com/renjithsmenon/pocketllm-examples/issues/new/choose). Issues are public, so never paste your API key or prompts.
- **API reference:** https://renjithsmenon.github.io/pocketllm-examples/api/
- **Compatible models:** https://renjithsmenon.github.io/pocketllm-examples/models/
- **Privacy policy:** https://renjithsmenon.github.io/pocketllm-examples/privacy/

The examples are MIT licensed.
