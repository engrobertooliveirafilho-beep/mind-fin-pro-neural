$ErrorActionPreference = "Stop"
Write-Host "Testando /health..." -ForegroundColor Cyan
Invoke-RestMethod http://localhost:8010/health
Write-Host "Checando métricas mindfin_requests_total..." -ForegroundColor Cyan
Invoke-WebRequest http://localhost:8010/metrics -UseBasicParsing | Select-String mindfin_requests_total
