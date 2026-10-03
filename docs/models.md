---
title: Compatible models
permalink: /models/
---

# Compatible models

PocketLLM runs **single-file GGUF** models on the iPhone with llama.cpp and
Apple Metal. Whether a model runs depends on its architecture, quantization,
context size and the memory iOS allows the app; PocketLLM checks what it can
before loading and explains any failure.

## Download in the app

These models are listed under **Models → Recommended** and download directly
from Hugging Face. All are Apache-2.0 or MIT licensed and need no account.

| Model | Size (Q4_K_M) | Licence | Notes |
|---|---|---|---|
| Qwen3 4B Instruct 2507 | 2.3 GB | Apache-2.0 | **Tested** on iPhone 17 Pro: chat, streaming, tool calling |
| Qwen2.5 0.5B Instruct | 0.5 GB | Apache-2.0 | Tested: chat, streaming, tool calling. Smallest and fastest |
| SmolLM2 1.7B Instruct | 1.0 GB | Apache-2.0 | |
| Qwen2.5 1.5B Instruct | 1.0 GB | Apache-2.0 | Multilingual |
| Qwen3 1.7B | 1.2 GB | Apache-2.0 | Reasoning |
| Phi-3.5 Mini Instruct | 2.2 GB | MIT | |
| Phi-4 Mini Instruct | 2.3 GB | MIT | Reasoning |
| Mistral 7B Instruct v0.3 | 4.1 GB | Apache-2.0 | Needs a recent iPhone with more memory |
| Qwen2.5 7B Instruct | 4.4 GB | Apache-2.0 | Needs a recent iPhone with more memory |
| Qwen3 8B | 4.7 GB | Apache-2.0 | Needs a recent iPhone with more memory |

Expand any model in the app to see whether it fits your iPhone's memory right
now (an estimate, shown as such).

## Import your own

Tap **+** in the Model Library to import any `.gguf` file from Files.

- **Single file only.** Split archives (`model-00001-of-00002.gguf`) must be
  merged first.
- **Mainstream architectures** supported by llama.cpp (Llama, Qwen, Gemma,
  Mistral, Phi and others) generally work. A very new architecture may need an
  app update; if a model can't load, the app says why.
- **Quantization:** start with **Q4_K_M**. Q5 and Q8 use more memory for
  modest quality gains; Q3 and Q2 fit larger models at lower quality.
- **Tool calling** works only when the model's own chat template supports it.
  The app shows this on each model's details screen.
