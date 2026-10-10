# Start Second Nurse with optional local secrets (gitignored .env.local).
# Usage: .\scripts\start-local.ps1
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

$envFile = Join-Path $Root ".env.local"
if (Test-Path $envFile) {
    Get-Content $envFile | ForEach-Object {
        if ($_ -match '^\s*#' -or $_ -match '^\s*$') { return }
        $pair = $_ -split '=', 2
        if ($pair.Count -eq 2) {
            $name = $pair[0].Trim()
            $value = $pair[1].Trim().Trim('"').Trim("'")
            Set-Item -Path "Env:$name" -Value $value
        }
    }
    Write-Host "Loaded $envFile"
}

if (-not $env:WARD_MCP_TOKEN) {
    $bytes = New-Object byte[] 32
    [System.Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($bytes)
    $env:WARD_MCP_TOKEN = [Convert]::ToBase64String($bytes)
    Write-Host "Generated ephemeral WARD_MCP_TOKEN for this session (persist in .env.local for AgntID runtime)."
}

if (-not $env:WARD_ALLOWED_HOSTS) {
    $env:WARD_ALLOWED_HOSTS = "host.docker.internal:3000"
}

if (-not $env:PORT) { $env:PORT = "3000" }

$venvUvicorn = Join-Path $Root ".venv\Scripts\uvicorn.exe"
if (-not (Test-Path $venvUvicorn)) {
    Write-Error "Missing .venv. Run: python -m venv .venv; pip install -r requirements.lock"
}

Write-Host "Starting Second Nurse on port $($env:PORT) ..."
& $venvUvicorn server.app:app --host 0.0.0.0 --port $env:PORT
