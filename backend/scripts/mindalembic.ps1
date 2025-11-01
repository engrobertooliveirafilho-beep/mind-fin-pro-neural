param(
  [ValidateSet("history","current","upgrade","downgrade","revision","stamp")]
  [string]$action = "current",
  [string]$message = ""
)

# habilita erros para parar na primeira falha
$ErrorActionPreference = "Stop"

# ativa venv e envs
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = (Get-Location).Path
$env:DATABASE_URL = "sqlite:///C:/MIND_MVP_BUILD/MIND_FIN_PRO/backend/mindfin.db"

switch ($action) {
  "history"   { python -m alembic history }
  "current"   { python -m alembic current }
  "upgrade"   { python -m alembic upgrade head }
  "downgrade" { python -m alembic downgrade -1 }
  "revision"  {
      if (-not $message) { Write-Error "Informe -message para revision"; exit 1 }
      python -m alembic revision --autogenerate -m "$message"
  }
  "stamp"     { python -m alembic stamp head }
}
