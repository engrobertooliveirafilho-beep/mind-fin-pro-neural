param(
  [int]$Port=8002,
  [switch]$Migrate,
  [switch]$NoReload
)

$ErrorActionPreference="Stop"
cd C:\MIND_MVP_BUILD\MIND_FIN_PRO\backend

if (!(Test-Path .\scripts\killmind.ps1) -or !(Test-Path .\scripts\runmind.ps1) -or !(Test-Path .\scripts\testmind.ps1) -or !(Test-Path .\scripts\mindlogin.ps1)) {
  throw "Scripts base ausentes."
}

# 1) liberar porta
.\scripts\killmind.ps1 $Port | Out-Host

# 2) abrir servidor em nova janela elevada (evita bloqueios de porta/ACL)
$reload = $NoReload.IsPresent  " --reload"
$maybeMig = $(if($Migrate){'python -m alembic upgrade head; ' } else { '' })
$cmd = @(
  '-NoExit',
  '-Command',
  'cd C:\MIND_MVP_BUILD\MIND_FIN_PRO\backend; ' +
  '.\.venv\Scripts\Activate.ps1; ' +
  '$env:PYTHONPATH=(Get-Location).Path; ' +
  "$env:DATABASE_URL='sqlite:///C:/MIND_MVP_BUILD/MIND_FIN_PRO/backend/mindfin.db'; " +
  $maybeMig +
  "python -m uvicorn app.temp_app:app --host 127.0.0.1 --port $Port --log-level debug$reload"
)
Start-Process powershell -Verb RunAs -ArgumentList $cmd | Out-Null

# 3) esperar subir /health
$base = "http://127.0.0.1:$Port"
$ok = $false
for($i=0;$i -lt 30;$i++){
  try {
    $h = Invoke-RestMethod "$base/health" -TimeoutSec 2
    if ($h.status -eq "ok") { $ok = $true; break }
  } catch {}
  Start-Sleep -Seconds 1
}
if (-not $ok) { throw "Servidor nÃ£o respondeu /health a tempo." }

# 4) testes smoke
.\scripts\testmind.ps1 $Port | Out-Host

# 5) login admin (mostra token)
"==> TOKEN ADMIN"
.\scripts\mindlogin.ps1 -Port $Port | Out-Host

Write-Host "âœ… OneMind completo. Servidor em $base"
