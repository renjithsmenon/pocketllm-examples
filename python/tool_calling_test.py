"""
Python test client for PocketLLM Server running on an iPhone.

Covers the path your agent will actually take: streaming chat, and a full
tool-calling round trip where the laptop executes the tool and feeds the
observation back. The iPhone only ever performs inference.

    pip install openai
    python test_client.py --host 192.168.1.25 --key sk-xxxx

Run --check first to confirm connectivity without spending a generation:

    python test_client.py --host 192.168.1.25 --key sk-xxxx --check
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request


def http_json(url: str, key: str, payload: dict | None = None) -> dict:
    data = json.dumps(payload).encode() if payload else None
    request = urllib.request.Request(url, data=data, method="POST" if data else "GET")
    request.add_header("Authorization", f"Bearer {key}")
    if data:
        request.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(request, timeout=300) as response:
        return json.loads(response.read())


def check(base: str, key: str) -> bool:
    """Health and model listing, with readable failures."""
    try:
        health = http_json(f"{base}/health", key)
    except urllib.error.URLError as error:
        print(f"Could not reach {base}/health: {error}")
        print("Check the phone is on the same Wi-Fi and the server is started.")
        return False

    print(f"health    : {json.dumps(health)}")
    if not health.get("model_loaded"):
        print("No model is loaded. Load one in the app first.")
        return False

    models = http_json(f"{base}/v1/models", key)
    for model in models["data"]:
        mark = "*" if model.get("loaded") else " "
        print(f"  {mark} {model['id']}")
    return True


def stream_chat(base: str, key: str, model: str, prompt: str, max_tokens: int) -> None:
    """Raw SSE read, so time-to-first-token is measured rather than assumed."""
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "stream": True,
    }
    request = urllib.request.Request(
        f"{base}/v1/chat/completions",
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )

    started = time.monotonic()
    first_token: float | None = None
    chunks = 0

    with urllib.request.urlopen(request, timeout=300) as response:
        for raw in response:
            line = raw.decode("utf-8").strip()
            if not line.startswith("data: "):
                continue
            body = line[6:]
            if body == "[DONE]":
                break

            chunk = json.loads(body)
            if "error" in chunk:
                print(f"\nserver error: {chunk['error']['message']}")
                return

            delta = chunk["choices"][0].get("delta", {})
            content = delta.get("content")
            if content:
                if first_token is None:
                    first_token = time.monotonic() - started
                chunks += 1
                print(content, end="", flush=True)

    total = time.monotonic() - started
    print(f"\n\n  {chunks} chunks | TTFT {first_token:.2f}s | total {total:.1f}s")


# --------------------------------------------------------------- tool calling

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_device_status",
            "description": "Return the current operational status of a device by its identifier.",
            "parameters": {
                "type": "object",
                "properties": {
                    "device_id": {"type": "string", "description": "Device identifier"},
                },
                "required": ["device_id"],
            },
        },
    }
]


def execute_tool(name: str, arguments: dict) -> dict:
    """
    Stand-in for whatever your agent actually runs.

    This is the point of the whole architecture: the tool executes **here**, on
    the laptop. The iPhone selected it but never runs it and never needs any
    access to the lab network.
    """
    if name == "get_device_status":
        return {"device_id": arguments.get("device_id"), "status": "running", "uptime_hours": 412}
    return {"error": f"unknown tool {name}"}


def tool_round_trip(base: str, key: str, model: str) -> None:
    messages = [
        {"role": "system", "content": "Use the provided tools when they are relevant."},
        {"role": "user", "content": "What is the status of device PLC-01?"},
    ]

    print("\n-- turn 1: asking the model to choose a tool")
    first = http_json(
        f"{base}/v1/chat/completions",
        key,
        {"model": model, "messages": messages, "tools": TOOLS, "tool_choice": "auto", "max_tokens": 256},
    )

    choice = first["choices"][0]
    tool_calls = choice["message"].get("tool_calls")

    if not tool_calls:
        print("The model answered without selecting a tool:")
        print(f"  {choice['message'].get('content')}")
        print("\nNot every GGUF can emit tool_calls. Check the model's Chat Template")
        print("section in the app — it reports the real capability.")
        return

    call = tool_calls[0]
    arguments = json.loads(call["function"]["arguments"] or "{}")
    print(f"  model selected: {call['function']['name']}({arguments})")

    print("-- laptop executes the tool")
    result = execute_tool(call["function"]["name"], arguments)
    print(f"  result: {result}")

    messages.append(choice["message"])
    messages.append(
        {"role": "tool", "tool_call_id": call.get("id", "call_1"), "content": json.dumps(result)}
    )

    print("-- turn 2: feeding the observation back")
    second = http_json(
        f"{base}/v1/chat/completions", key, {"model": model, "messages": messages, "max_tokens": 256}
    )
    print(f"\n  {second['choices'][0]['message']['content']}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", required=True, help="iPhone LAN IP address")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--key", required=True, help="Bearer token from the app")
    parser.add_argument("--prompt", default="Reply with exactly: hello")
    parser.add_argument("--max-tokens", type=int, default=128)
    parser.add_argument("--check", action="store_true", help="Connectivity only")
    parser.add_argument("--tools", action="store_true", help="Run the tool-calling round trip")
    args = parser.parse_args()

    base = f"http://{args.host}:{args.port}"
    if not check(base, args.key):
        return 1
    if args.check:
        return 0

    model = http_json(f"{base}/health", args.key)["model"]

    if args.tools:
        tool_round_trip(base, args.key, model)
    else:
        print(f"\n-- streaming from {model}\n")
        stream_chat(base, args.key, model, args.prompt, args.max_tokens)

    print(f"\nmetrics   : {json.dumps(http_json(f'{base}/metrics', args.key))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
