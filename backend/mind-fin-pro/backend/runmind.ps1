param(
  [switch]$Rebuild
)
$root = "C:\MIND_MVP_BUILD\MIND_FIN_PRO\backend\mind-fin-pro"
Set-Location $root

Write-Host ">> Verificando Docker daemon..." -ForegroundColor Cyan
try { docker info | Out-Null } catch { throw "Docker não está rodando. Inicie o Docker Desktop e tente novamente." }

if ($Rebuild) {
  Write-Host ">> docker compose up -d --build" -ForegroundColor Yellow
  docker compose up -d --build
} else {
  Write-Host ">> docker compose up -d" -ForegroundColor Yellow
  docker compose up -d
}

Write-Host "`nContainers:" -ForegroundColor Green
docker compose ps

Write-Host "`nEndpoints:" -ForegroundColor Magenta
Write-Host "API ............. http://localhost:8000"
Write-Host "Grafana ......... http://localhost:3000"
Write-Host "Prometheus ...... http://localhost:9090"
