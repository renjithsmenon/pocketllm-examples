---
title: Privacy Policy
permalink: /privacy/
---

# PocketLLM Server: Privacy Policy

**Effective date:** 4 October 2026

PocketLLM Server turns your iPhone into a local AI inference server. This
policy explains what the app does with data.

## Your prompts and responses stay on your device

Models run on your iPhone. Requests from your computers and apps reach the
iPhone over your local network, and responses go back the same way.
PocketLLM never sends prompts, responses or model files to us or to any cloud
service.

By default, the app's request history records only metadata: time, endpoint,
status, token counts, timings, and the local network address of the client
that sent the request. It's kept in memory on the iPhone and cleared when you
clear it or close the app. If you turn on **Settings → Developer → Log Request
Content**, prompt and response text is also kept in that on-device history
until you clear it.

## Model downloads

When you tap Download in the Model Library, PocketLLM fetches that model file
directly from Hugging Face (huggingface.co), which sees a standard download
request from your device, as with any website. Nothing else is sent. Models
are stored only on your iPhone and are excluded from device backups.

## Anonymous usage statistics

To learn whether people can get from installing the app to their first
successful request, PocketLLM sends anonymous usage statistics to
TelemetryDeck (telemetrydeck.com). They include:

- events such as "onboarding completed", "model loaded", "server started"
  and "first external request", and paywall and purchase events (viewed,
  trial started, purchase completed, restored)
- coarse ranges, such as model size "2–4 GB" or response time "250–500 ms",
  the model architecture and quantization names from the file header, and
  the app version
- a random identifier created when the app is installed, hashed before it
  is sent

They never include prompts, responses, model file names, API keys, IP
addresses, network names, product IDs, prices or offer codes. You can turn
statistics off in **Settings → Privacy**. Turning them off deletes the random
identifier and any unsent events.

## Purchases

Purchases and offer-code redemptions are handled entirely by Apple. PocketLLM
receives only Apple's confirmation of what you're entitled to; it never sees
your payment details or the codes you redeem. The 7-day trial is recorded
only on your iPhone.

## What we don't do

We don't sell data, show ads, track you across apps or websites, or ask for
your contacts, location or other personal information.

## API keys

The API key that protects your server is generated on the device and stored in
the iOS Keychain. It is never sent to us.

## Contact

Questions or requests about privacy: open an issue at
[github.com/renjithsmenon/pocketllm-examples/issues](https://github.com/renjithsmenon/pocketllm-examples/issues).
Issues are public, so don't include personal information. For a privacy
request, open an issue titled "Privacy request" without details and we'll
respond there.

## Changes

We'll update this page if the app's data practices change, and the effective
date above will change with it.
