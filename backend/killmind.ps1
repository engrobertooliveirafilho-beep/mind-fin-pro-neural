Write-Host "Encerrando Mind API..." -ForegroundColor Red
$job = Get-Job | Where-Object { $_.Name -eq "MindAPI" }
if ($job) {
  Stop-Job $job -ErrorAction SilentlyContinue
  Remove-Job $job -ErrorAction SilentlyContinue
  Write-Host "Job MindAPI parado." -ForegroundColor Green
} else {
  Write-Host "Nenhum job MindAPI encontrado." -ForegroundColor Yellow
}

# fallback: mata qualquer processo ouvindo na 8010
Get-NetTCPConnection -LocalPort 8010 -State Listen -ErrorAction SilentlyContinue |
  ForEach-Object {
    $procId = $_.OwningProcess
    if ($procId) { try { Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue } catch {} }
  }
Write-Host "OK." -ForegroundColor Green
