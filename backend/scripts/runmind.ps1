param([int]$Port=8002, [switch]$NoReload)

$ErrorActionPreference="Stop"
cd C:\MIND_MVP_BUILD\MIND_FIN_PRO\backend
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = (Get-Location).Path
$env:DATABASE_URL = 'sqlite:///C:/MIND_MVP_BUILD/MIND_FIN_PRO/backend/mindfin.db'

if (Test-Path .\scripts\killmind.ps1) { & .\scripts\killmind.ps1 $Port | Out-Host }

python -m alembic upgrade head | Out-Host

$reload = $NoReload.IsPresent ? "" : " --reload"
python -m uvicorn app.temp_app:app --host 127.0.0.1 --port $Port --log-level debug$reload
