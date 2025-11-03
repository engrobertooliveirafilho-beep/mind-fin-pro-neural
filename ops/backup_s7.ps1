param(
  [string]$Project="C:\MIND_MVP_BUILD\MIND_FIN_PRO",
  [string]$OutDir ="C:\MIND_MVP_BUILD\MIND_FIN_PRO\backups"
)

if (!(Test-Path $OutDir)) { New-Item -ItemType Directory -Path $OutDir -Force | Out-Null }

# Coletar apenas caminhos existentes
$items = @()
if (Test-Path "$Project\data")            { $items += "$Project\data\*" }
if (Test-Path "$Project\frontend\dist")   { $items += "$Project\frontend\dist\*" }
if (Test-Path "$Project\ops")             { $items += "$Project\ops\*.json" }

if ($items.Count -eq 0) {
  Write-Warning "Nada para arquivar (data/dist/ops ausentes)."
  exit 0
}

$ts  = Get-Date -Format yyyyMMdd_HHmmss
$zip = Join-Path $OutDir "mind_$ts.zip"

Compress-Archive -Path $items -DestinationPath $zip -CompressionLevel Optimal -Force
Write-Host "Backup OK -> $zip"
