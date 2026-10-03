# One chat completion against PocketLLM Server (Windows PowerShell 5.1 or 7).

$body = @{
  model    = "local-model"
  messages = @(@{ role = "user"; content = "Say hello in one short sentence." })
} | ConvertTo-Json -Depth 5

$response = Invoke-RestMethod -Method Post `
  -Uri "http://IPHONE_IP:8080/v1/chat/completions" `
  -Headers @{ Authorization = "Bearer YOUR_API_KEY" } `
  -ContentType "application/json" -Body $body
$response.choices[0].message.content
