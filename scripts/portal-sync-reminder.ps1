# Reminds you to sync host ward token with the AgntID portal (no secrets printed).
$envFile = Join-Path (Split-Path -Parent $PSScriptRoot) ".env.local"
if (-not (Test-Path $envFile)) {
    Write-Host "Create .env.local from .env.local.example first."
    exit 1
}
Write-Host @"

Portal checklist (see docs/WINDOWS-PORTAL-INTEGRATION.md):

1. Copy WARD_MCP_TOKEN from .env.local into a runtime-side secret env var.
2. Add Remote HTTP MCP: http://host.docker.internal:3000/mcp with Bearer referencing that secret.
3. Review nine ward tools + Medium/READ_WRITE + numeric bounds; wait for APPLIED.
4. Restart Second Nurse if you change .env.local, then: python scripts/live_smoke.py

"@
Write-Host "WARD_MCP_TOKEN is set in .env.local: $((Select-String -Path $envFile -Pattern '^WARD_MCP_TOKEN=').Line -ne $null)"
