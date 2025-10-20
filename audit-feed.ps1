# audit-feed.ps1
param(
    [int]$IntervalSeconds = 6,
    [int]$MaxEntries = 100
)

$PUBLIC_JSON = Join-Path $PWD 'public\MIND_AUDIT_ENRICHED.json'
$eventTypes = @('OK','WARN','INFO','ERROR')
$modules = @('dopamine_core','analytics_core','audit_main','inflow','neuro_sync')

# Garante JSON inicial válido
if (!(Test-Path $PUBLIC_JSON)) {
    '{"version":"v0.1.3","entries":[]}' | Set-Content -Encoding UTF8 $PUBLIC_JSON
}

Write-Host "▶ Alimentando $PUBLIC_JSON a cada $IntervalSeconds s (Ctrl+C para parar)...`n" -ForegroundColor Cyan

while ($true) {
    try {
        # Lê e converte o JSON atual
        $state = Get-Content $PUBLIC_JSON -Raw | ConvertFrom-Json
        if (-not $state.entries) { $state.entries = @() }

        # Cria um novo evento simulado
        $id = if ($state.entries.Count -gt 0) { ($state.entries | Sort-Object id -Descending | Select-Object -First 1).id + 1 } else { 1 }
        $timestamp = (Get-Date).ToString('yyyy-MM-dd HH:mm:ss')
        $status = Get-Random -InputObject $eventTypes
        $origin = Get-Random -InputObject $modules
        $message = switch ($status) {
            'OK'    { "Módulo $origin validado com sucesso." }
            'WARN'  { "Latência acima do limite em $origin." }
            'INFO'  { "Nova métrica registrada em $origin." }
            'ERROR' { "Falha crítica detectada em $origin!" }
        }

        $entry = [pscustomobject]@{
            id = $id
            timestamp = $timestamp
            title = "Evento automático #$id"
            file = "$origin.py"
            origin = $origin
            message = $message
            status = $status
        }

        # Adiciona o novo evento ao início
        $state.entries = ,$entry + $state.entries | Select-Object -First $MaxEntries
        $jsonOut = $state | ConvertTo-Json -Depth 5
        $jsonOut | Set-Content -Encoding UTF8 $PUBLIC_JSON

        Write-Host "[{0}] +{1} ({2}) {3}" -f $timestamp, $id, $status, $message -ForegroundColor Green
    }
    catch {
        Write-Warning "⚠ Falha ao atualizar JSON: $_"
    }

    Start-Sleep -Seconds $IntervalSeconds
}
