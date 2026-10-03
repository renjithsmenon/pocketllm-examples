---
title: API reference
permalink: /api/
---

# API reference

PocketLLM Server speaks a subset of the OpenAI API over plain HTTP on your
local network. The base URL is shown on the app's Server tab:
`http://<iphone-ip>:8080/v1` (the port is configurable in Server Settings).

## Authentication

Send the app's API key as a bearer token:

```
Authorization: Bearer sk-…
```

`/health` needs no key, so clients can check connectivity separately from
authentication. Authentication can be turned off in the app (not recommended:
anyone on the network could then use the server).

## Endpoints

| Endpoint | Auth | Purpose |
|---|---|---|
| `GET /health` | no | Liveness, loaded model, context size, Metal status |
| `GET /v1/models` | yes | Models on the device; the loaded one has `"loaded": true` |
| `POST /v1/chat/completions` | yes | Chat, streaming, tool calls, structured output |
| `GET /metrics` | yes | Request counters and the last request's timings |

## Chat completions

Supported request fields:

| Field | Notes |
|---|---|
| `model` | The loaded model's id from `/v1/models`, or a generic name such as `local-model`, `default` or `gpt-4o` (all mean "the loaded model") |
| `messages` | Roles `system`, `user`, `assistant`, `tool` |
| `stream` | `true` for server-sent events, ending with `data: [DONE]` |
| `max_tokens`, `temperature`, `top_p`, `stop` | Defaults come from the app's Settings |
| `tools`, `tool_choice` | Only for models whose chat template supports tool calls; otherwise `400 tools_unsupported` |
| `response_format` | `json_object` or `json_schema` for structured output |

Responses follow OpenAI's shape, including `usage` token counts. One request
is generated at a time; a second concurrent request receives `429`.

## Errors

Errors use OpenAI's envelope:
`{"error": {"message": "…", "type": "…", "code": "…"}}`.

| Status | Code | Meaning |
|---|---|---|
| 400 | `invalid_json`, `invalid_parameter`, `malformed_request` | The request body or a field is invalid |
| 400 | `tools_unsupported` | The loaded model can't express tool calls |
| 400 | `template_unsupported` | The model's chat template couldn't be applied |
| 401 | `missing_api_key`, `invalid_api_key` | No key, or the wrong key |
| 404 | `unknown_route` | No such endpoint |
| 404 | `model_not_found` | `model` names a model that isn't loaded |
| 405 | `method_not_allowed` | Wrong HTTP method for the endpoint |
| 429 | `model_busy` | Another request is generating |
| 499 | `request_cancelled` | The client disconnected or the generation was cancelled |
| 503 | `model_not_loaded` | No model is loaded |
| 503 | `insufficient_memory`, `context_allocation_failed` | Not enough memory for the model or context |
| 500 | `internal_error` and others | An unexpected server or inference error |

## Examples

Working Python, JavaScript, PowerShell and curl examples, including a full
tool-calling round trip, are in the
[examples repository](https://github.com/renjithsmenon/pocketllm-examples).
