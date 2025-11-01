# mind.ps1  (PowerShell 5.1 compatível)
$global:MINDFIN_ROOT = "C:\MIND_MVP_BUILD\MIND_FIN_PRO\backend\mind-fin-pro\backend"
$global:PYTHON      = Join-Path $MINDFIN_ROOT ".venv\Scripts\python.exe"
$global:UVICORN     = Join-Path $MINDFIN_ROOT ".venv\Scripts\uvicorn.exe"
$global:BASE_URL    = "http://127.0.0.1:8000"
$global:WS_URL      = "ws://127.0.0.1:8000/ws/ai"

function Setup-Venv {
    Set-Location $MINDFIN_ROOT
    if (-not (Test-Path ".venv")) { python -m venv .venv }
    & $PYTHON -m pip install --upgrade pip
    & $PYTHON -m pip install fastapi uvicorn pydantic apscheduler cryptography prometheus_client
}

function runmind {
    Set-Location $MINDFIN_ROOT

    if (-not $env:LOG_AES_KEY -or $env:LOG_AES_KEY -eq "") { $env:LOG_AES_KEY = "teste" }
    if (-not $env:LOG_AES_IV  -or $env:LOG_AES_IV  -eq "") { $env:LOG_AES_IV  = "teste" }

    Setup-Venv

    netstat -ano | findstr :8000 | % { $pid = ($_ -split "\s+")[-1]; Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue }

    Write-Host ">> Iniciando MIND FIN PRO @ 127.0.0.1:8000" -ForegroundColor Cyan
    & $UVICORN app:app --host 127.0.0.1 --port 8000 --log-level info
}

function killmind {
    Write-Host ">> Encerrando processos na porta 8000" -ForegroundColor Yellow
    netstat -ano | findstr :8000 | % { $pid = ($_ -split "\s+")[-1]; Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue }
}

function Test-Http($Method, $Url, $BodyObj=$null) {
    try {
        if ($BodyObj -ne $null) {
            $json = $BodyObj | ConvertTo-Json -Depth 5
            $res = Invoke-RestMethod -Method $Method -Uri $Url -Body $json -ContentType "application/json"
        } else {
            $res = Invoke-RestMethod -Method $Method -Uri $Url
        }
        Write-Host "√ $Method $Url -> OK" -ForegroundColor Green
        return $res
    } catch {
        Write-Host "× $Method $Url -> $($_.Exception.Message)" -ForegroundColor Red
        throw
    }
}

function Test-WebSocket {
    Add-Type -AssemblyName System.Net.Http
    Add-Type -AssemblyName System.Runtime
    Add-Type -AssemblyName System.Net.WebSockets

    $cws = [System.Net.WebSockets.ClientWebSocket]::new()
    $cts = [System.Threading.CancellationToken]::None
    $uri = [System.Uri]::new($global:WS_URL)
    try {
        $cws.ConnectAsync($uri, $cts).GetAwaiter().GetResult()
        $msg = "ping"
        $bytes = [System.Text.Encoding]::UTF8.GetBytes($msg)
        $seg = [System.ArraySegment[byte]]::new($bytes)
        $cws.SendAsync($seg, [System.Net.WebSockets.WebSocketMessageType]::Text, $true, $cts).GetAwaiter().GetResult()

        $buffer = New-Object byte[] 4096
        $recvSeg = [System.ArraySegment[byte]]::new($buffer)
        $result = $cws.ReceiveAsync($recvSeg, $cts).GetAwaiter().GetResult()
        $text = [System.Text.Encoding]::UTF8.GetString($buffer, 0, $result.Count)
        Write-Host "√ WS $($global:WS_URL) -> $text" -ForegroundColor Green
    } catch {
        Write-Host "× WS $($global:WS_URL) -> $($_.Exception.Message)" -ForegroundColor Red
        throw
    } finally {
        if ($cws.State -eq [System.Net.WebSockets.WebSocketState]::Open) {
            $cws.CloseAsync([System.Net.WebSockets.WebSocketCloseStatus]::NormalClosure, "bye", $cts).GetAwaiter().GetResult()
        }
        $cws.Dispose()
    }
}

function testmind {
    Write-Host "== MIND FIN PRO :: TESTES ==" -ForegroundColor Cyan

    try {
        Invoke-WebRequest -Uri "$global:BASE_URL/admin/metrics" -Method GET -UseBasicParsing | Out-Null
        Write-Host "√ Servidor responde" -ForegroundColor Green
    } catch {
        Write-Host "Servidor não respondeu. Vou tentar subir..." -ForegroundColor Yellow
        Start-Process -FilePath $PSCommandPath -ArgumentList "autorun" -WindowStyle Hidden | Out-Null
        Start-Sleep -Seconds 2
    }

    $r1 = Test-Http -Method GET -Url "$global:BASE_URL/debug/crypto?echo=ping"

    $payload = @{
        income = 6000
        expenses = 4200
        debt = 15000
        risk_profile = "moderado"
        mood = "neutro"
    }
    $r2 = Test-Http -Method POST -Url "$global:BASE_URL/simulate/performance" -BodyObj $payload

    try {
        $txt = Invoke-WebRequest -Uri "$global:BASE_URL/admin/metrics" -Method GET -UseBasicParsing
        Write-Host "√ GET /admin/metrics -> métricas recebidas" -ForegroundColor Green
    } catch {
        Write-Host "× GET /admin/metrics -> $($_.Exception.Message)" -ForegroundColor Red
        throw
    }

    try { Test-WebSocket } catch { }

    Write-Host "== TESTES CONCLUÍDOS ==" -ForegroundColor Cyan
}

if ($args.Length -gt 0 -and $args[0] -eq "autorun") {
    runmind
}
