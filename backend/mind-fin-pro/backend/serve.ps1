$ErrorActionPreference = 'Stop'
$proj = 'C:\MIND_MVP_BUILD\MIND_FIN_PRO\backend\mind-fin-pro\backend'
Set-Location $proj

# Desliga tracing local (evita WinError 10061 em :4318)
$env:OTEL_SDK_DISABLED = 'true'

# Ativa venv e inicia o server
. .\.venv\Scripts\Activate.ps1
python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
