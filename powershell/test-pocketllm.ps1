<#
.SYNOPSIS
    Exercises PocketLLM Server on the iPhone from Windows: health, models,
    chat and a real streaming check.

.EXAMPLE
    .\Test-LlmServer.ps1 -IPhoneIp 192.168.1.25 -ApiKey sk-xxxx

.EXAMPLE
    .\Test-LlmServer.ps1 -IPhoneIp 192.168.1.25 -ApiKey sk-xxxx -Prompt "List three OT protocols."
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$IPhoneIp,
    [Parameter(Mandatory)][string]$ApiKey,
    [int]$Port = 8080,
    [string]$Prompt = "Reply with exactly: hello",
    [int]$MaxTokens = 64
)

$ErrorActionPreference = 'Stop'
$base = "http://${IPhoneIp}:${Port}"
$headers = @{ Authorization = "Bearer $ApiKey" }

function Write-Step([string]$Text) {
    Write-Host ""
    Write-Host "== $Text " -NoNewline -ForegroundColor Cyan
    Write-Host ("=" * [Math]::Max(0, 58 - $Text.Length)) -ForegroundColor DarkGray
}

# ---------------------------------------------------------------- 1. health
Write-Step "GET /health"
try {
    $health = Invoke-RestMethod -Uri "$base/health" -Headers $headers -TimeoutSec 10
    $health | Format-List
    if (-not $health.model_loaded) {
        Write-Host "No model is loaded. Load one in the app before continuing." -ForegroundColor Yellow
        return
    }
}
catch {
    Write-Host "Could not reach $base/health" -ForegroundColor Red
    Write-Host "  $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "  Check the phone is on the same Wi-Fi and the server is started." -ForegroundColor Yellow
    return
}

# ---------------------------------------------------------------- 2. models
Write-Step "GET /v1/models"
$models = Invoke-RestMethod -Uri "$base/v1/models" -Headers $headers -TimeoutSec 10
$models.data | Format-Table id, loaded, architecture, context_length -AutoSize
$modelId = ($models.data | Where-Object { $_.loaded } | Select-Object -First 1).id

# ------------------------------------------------------------ 3. auth check
Write-Step "401 without a key"
try {
    Invoke-RestMethod -Uri "$base/v1/models" -TimeoutSec 10 | Out-Null
    Write-Host "UNEXPECTED: the request succeeded without a key." -ForegroundColor Red
}
catch {
    $code = $_.Exception.Response.StatusCode.value__
    if ($code -eq 401) { Write-Host "401 as expected" -ForegroundColor Green }
    else { Write-Host "Expected 401, got $code" -ForegroundColor Red }
}

# ------------------------------------------------- 4. buffered chat request
Write-Step "POST /v1/chat/completions (stream=false)"
$body = @{
    model       = $modelId
    messages    = @(
        @{ role = 'system'; content = 'You are a terse assistant.' }
        @{ role = 'user'; content = $Prompt }
    )
    temperature = 0.2
    max_tokens  = $MaxTokens
    stream      = $false
} | ConvertTo-Json -Depth 6

$sw = [Diagnostics.Stopwatch]::StartNew()
$response = Invoke-RestMethod -Uri "$base/v1/chat/completions" -Headers $headers `
    -Method Post -ContentType 'application/json' -Body $body -TimeoutSec 300
$sw.Stop()

Write-Host "Response:" -ForegroundColor Green
Write-Host $response.choices[0].message.content
Write-Host ""
Write-Host ("  prompt {0} / completion {1} tokens in {2:N1}s" -f `
        $response.usage.prompt_tokens, $response.usage.completion_tokens, $sw.Elapsed.TotalSeconds)

# ----------------------------------------------------- 5. streaming request
Write-Step "POST /v1/chat/completions (stream=true)"
# Invoke-RestMethod buffers the whole body, which would defeat the point.
# Read the raw stream so the real time-to-first-token is visible.
$streamBody = @{
    model      = $modelId
    messages   = @(@{ role = 'user'; content = $Prompt })
    max_tokens = $MaxTokens
    stream     = $true
} | ConvertTo-Json -Depth 6

$request = [System.Net.HttpWebRequest]::Create("$base/v1/chat/completions")
$request.Method = 'POST'
$request.ContentType = 'application/json'
$request.Headers.Add('Authorization', "Bearer $ApiKey")
$request.Timeout = 300000
$request.ReadWriteTimeout = 300000

$bytes = [Text.Encoding]::UTF8.GetBytes($streamBody)
$request.ContentLength = $bytes.Length
$requestStream = $request.GetRequestStream()
$requestStream.Write($bytes, 0, $bytes.Length)
$requestStream.Close()

$sw = [Diagnostics.Stopwatch]::StartNew()
$firstToken = $null
$tokenCount = 0

$reader = New-Object IO.StreamReader($request.GetResponse().GetResponseStream())
try {
    while (-not $reader.EndOfStream) {
        $line = $reader.ReadLine()
        if (-not $line.StartsWith('data: ')) { continue }

        $payload = $line.Substring(6)
        if ($payload -eq '[DONE]') { break }

        $chunk = $payload | ConvertFrom-Json
        $delta = $chunk.choices[0].delta
        if ($delta.PSObject.Properties.Name -contains 'content' -and $delta.content) {
            if ($null -eq $firstToken) {
                $firstToken = $sw.Elapsed.TotalSeconds
                Write-Host ("  first token after {0:N2}s" -f $firstToken) -ForegroundColor DarkGray
            }
            $tokenCount++
            Write-Host -NoNewline $delta.content
        }
    }
}
finally {
    $reader.Close()
}
$sw.Stop()

Write-Host ""
Write-Host ""
Write-Host ("  {0} chunks, TTFT {1:N2}s, total {2:N1}s" -f `
        $tokenCount, $firstToken, $sw.Elapsed.TotalSeconds) -ForegroundColor Green

if ($firstToken -and $sw.Elapsed.TotalSeconds - $firstToken -gt 0.2) {
    Write-Host "  Tokens arrived progressively -- streaming is real." -ForegroundColor Green
}

# --------------------------------------------------------------- 6. metrics
Write-Step "GET /metrics"
Invoke-RestMethod -Uri "$base/metrics" -Headers $headers -TimeoutSec 10 | Format-List
