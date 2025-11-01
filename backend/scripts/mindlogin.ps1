param(
  [int]$Port=8002,
  [string]$Email="admin@mind.com",
  [string]$Password="123456",
  [string]$Name="Admin"
)

$base = "http://127.0.0.1:$Port"

# tenta criar (ignora conflito)
try {
  $user = @{name=$Name; email=$Email; password=$Password; bio=""; ai_profile=""} | ConvertTo-Json
  Invoke-RestMethod "$base/users/" -Method POST -ContentType "application/json" -Body $user | Out-Null
} catch {}

$login = @{email=$Email; password=$Password} | ConvertTo-Json
$resp = Invoke-RestMethod "$base/users/login" -Method POST -ContentType "application/json" -Body $login
"ACCESS_TOKEN=$($resp.access_token)"
