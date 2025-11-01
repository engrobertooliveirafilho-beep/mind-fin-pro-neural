$ErrorActionPreference = "Stop"

# --- paths
$backend = "C:\MIND_MVP_BUILD\MIND_FIN_PRO\backend"
$venvPy  = "C:\MIND_MVP_BUILD\MIND_FIN_PRO\venv\Scripts\python.exe"
$activate= "C:\MIND_MVP_BUILD\MIND_FIN_PRO\venv\Scripts\Activate.ps1"

Write-Host "Iniciando ambiente MIND..." -ForegroundColor Yellow

if (!(Test-Path $venvPy)) {
  Write-Host "ERRO: venv não encontrado em $venvPy" -ForegroundColor Red
  exit 1
}

# garante venv e PYTHONPATH
& $activate | Out-Null
$env:PYTHONPATH = $backend
Set-Location $backend

Write-Host "Subindo FastAPI na porta 8010..." -ForegroundColor Cyan

# mata job antigo se houver
$old = Get-Job | Where-Object { $_.Name -eq "MindAPI" }
if ($old) { Stop-Job $old -ErrorAction SilentlyContinue; Remove-Job $old -ErrorAction SilentlyContinue }

# sobe uvicorn em job
Start-Job -Name "MindAPI" -ScriptBlock {
  Push-Location "C:\MIND_MVP_BUILD\MIND_FIN_PRO\backend"
  & "C:\MIND_MVP_BUILD\MIND_FIN_PRO\venv\Scripts\python.exe" -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8010
} | Out-Null

Start-Sleep -Seconds 5

# smoke /health
try {
  $h = Invoke-RestMethod http://localhost:8010/health -TimeoutSec 5
  if ($h.status -eq "ok") {
    Write-Host "API MIND rodando em http://localhost:8010" -ForegroundColor Green
  } else {
    Write-Host "API respondeu: $($h.status)" -ForegroundColor Yellow
  }
} catch {
  Write-Host "Falha ao conectar no /health. Veja logs do job: Receive-Job -Name MindAPI -Keep | Select-Object -Last 80" -ForegroundColor Red
}

Write-Host ""
Write-Host "Comandos:" -ForegroundColor White
Write-Host "  .\testmind.ps1  -> testar /health e /metrics"
Write-Host "  .\killmind.ps1  -> encerrar servidor"
Write-Host ""
Write-Host "MIND DEV pronto - use: runmind | testmind | killmind" -ForegroundColor Yellow

