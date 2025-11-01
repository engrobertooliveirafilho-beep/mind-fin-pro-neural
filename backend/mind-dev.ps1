# ========== MIND DEV - FUNÇÕES LOCAIS ==========
$proj = "C:\MIND_MVP_BUILD\MIND_FIN_PRO\backend\mind-fin-pro\backend"

# Desliga OpenTelemetry local (para evitar o erro WinError 10061)
$env:OTEL_TRACES_EXPORTER = "none"
$env:OTEL_METRICS_EXPORTER = "none"
$env:OTEL_LOGS_EXPORTER   = "none"
$env:OTEL_EXPORTER_OTLP_ENDPOINT = ""

function RunMind {
    Set-Location $proj
    . .\.venv\Scripts\Activate.ps1
    $tcp = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue
    if ($tcp) { Stop-Process -Id $tcp.OwningProcess -Force }
    Write-Host "🚀 Uvicorn subindo em http://127.0.0.1:8000 ..."
    python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
}

function KillMind {
    $tcp = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue
    if ($tcp) { Stop-Process -Id $tcp.OwningProcess -Force; "✅ Matado PID $($tcp.OwningProcess)" }
    else { "ℹ️ Nada escutando na porta 8000." }
}

function TestMind {
    $body = '{"income":6000,"expenses":4200,"debt":15000,"risk_profile":"moderado","mood":"neutro"}'
    Invoke-RestMethod -Uri 'http://127.0.0.1:8000/simulate/performance' -Method Post -Body $body -ContentType 'application/json'
}

Set-Alias runmind  RunMind  -Scope Global -Force
Set-Alias killmind KillMind -Scope Global -Force
Set-Alias testmind TestMind -Scope Global -Force

Write-Host "✅ MIND DEV carregado — comandos: runmind | killmind | testmind"
# ================================================
