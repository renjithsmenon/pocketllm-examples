# curl

Replace `IPHONE_IP` and `YOUR_API_KEY` with the values on the Server tab.

## Health (no key needed)

```sh
curl http://IPHONE_IP:8080/health
```

## List models

```sh
curl http://IPHONE_IP:8080/v1/models -H 'Authorization: Bearer YOUR_API_KEY'
```

## Streaming chat completion

```sh
curl -N 'http://IPHONE_IP:8080/v1/chat/completions' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{"model":"local-model","stream":true,"messages":[{"role":"user","content":"Say hello in one short sentence."}]}'
```
