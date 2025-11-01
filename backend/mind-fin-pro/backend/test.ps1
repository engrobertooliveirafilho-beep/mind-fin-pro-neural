$body = '{"income":6000,"expenses":4200,"debt":15000,"risk_profile":"moderado","mood":"neutro"}'
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/simulate/performance' -Method Post -Body $body -ContentType 'application/json'
