$tcp = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue
if ($tcp) { Stop-Process -Id $tcp.OwningProcess -Force; "Matado PID $($tcp.OwningProcess)" } else { "Nada escutando na 8000." }
