---
title: Support
permalink: /support/
---

# Support

## Get help

Open an issue on GitHub:
**[github.com/renjithsmenon/pocketllm-examples/issues](https://github.com/renjithsmenon/pocketllm-examples/issues)**

You'll need a free GitHub account. Choose the template that fits: bug report,
model compatibility, or question.

> **Issues are public. Never paste your API key, your prompts, or anything
> personal.** An API key in a public issue lets anyone on your network use
> your server. If you shared one by accident, regenerate it in PocketLLM:
> **Settings → API Key → Regenerate API Key**.

Helpful details to include:

- iPhone model and iOS version
- PocketLLM version (**Settings → About**)
- The model you were using (name and size)
- What you did, what you expected, and what happened
- For connection problems: the client (Python, curl, an agent framework…) and
  the HTTP status code you received

## Troubleshooting

**Connection refused or timing out**
- Check that the server is running and PocketLLM is open in the foreground.
  iOS pauses the server when the app is backgrounded or the phone locks.
  **Settings → Keep Screen On** helps.
- Make sure your computer and iPhone are on the **same Wi-Fi network**. Guest
  and many corporate networks isolate devices from each other.
- Use the exact endpoint shown on the Server tab; the iPhone's address can
  change when it reconnects to Wi-Fi.

**401 Unauthorized**
The API key is missing or wrong. Send it as `Authorization: Bearer <key>`.
If you regenerated the key in the app, update your clients.

**429 Too Many Requests (`model_busy`)**
PocketLLM generates one response at a time. Send requests one after another.

**503 Service Unavailable (`model_not_loaded`)**
No model is loaded. Load one in the **Models** tab.

**400 `tools_unsupported`**
The loaded model's chat template can't express tool calls. Load a model whose
template supports tools; each model's details show this.

**A model won't load**
It may need more memory than iOS allows the app. Try a smaller model or a
smaller quantization (Q4 rather than Q5/Q8), lower **Context Size** in
Settings, or close other apps. Expand a model in the Models tab to see its
estimated memory fit.

**A download stops or fails**
Downloads continue while you use other apps, but restart if PocketLLM is
force-quit mid-download. Tap **Resume** or **Retry**. Check you have enough
free storage.

## Frequently asked questions

**Which models work?** See [compatible models](../models/). Single-file GGUF
models with a mainstream architecture generally work; only models listed as
tested have been verified.

**How does pricing work?** Try everything free for 7 days with no payment
details. Then a one-time **Lifetime** purchase unlocks unlimited serving: no
subscription. Without it, PocketLLM keeps working and the server runs in
10-minute sessions.

**I bought Lifetime on another device or reinstalled.** Open **Settings →
Plan → Restore Purchases** while signed in with the same Apple ID.

**I have a code.** Open **Settings → Plan → Redeem Code**. Codes are redeemed
through Apple's own sheet.

**Is my data sent anywhere?** Inference runs on your iPhone; prompts and
responses are never sent to us or any cloud service. See the
[privacy policy](../privacy/).
