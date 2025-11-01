param([int]$Port=8002)
$ErrorActionPreference = "SilentlyContinue"

$me = $PID
$parents = @()
try { $pp = Get-CimInstance Win32_Process -Filter "ProcessId=$me"; if ($pp) { $parents += $pp.ParentProcessId } } catch {}

$cons = Get-NetTCPConnection -LocalPort $Port -State Listen
if (!$cons) { Write-Host "✅ Porta $Port já está livre."; exit 0 }

$owners = $cons | Select-Object -ExpandProperty OwningProcess -Unique
foreach($pid in $owners){
  if ($pid -eq $me -or $parents -contains $pid) { Write-Host "⏭️  Ignorando PID do shell: $pid"; continue }
  try {
    $proc = Get-Process -Id $pid -ErrorAction Stop
    Write-Host "🔪 Matando PID $pid ($($proc.ProcessName))..."
    Stop-Process -Id $pid -Force -ErrorAction Stop
  } catch {
    Start-Process -Verb RunAs -FilePath cmd.exe -ArgumentList "/c taskkill /PID $pid /F /T" -Wait | Out-Null
  }
}

Start-Sleep 1
if (Get-NetTCPConnection -LocalPort $Port -State Listen) {
  Write-Host "❌ Porta $Port ainda ocupada. Abra como Administrador."; exit 1
}
Write-Host "✅ Porta $Port liberada."
