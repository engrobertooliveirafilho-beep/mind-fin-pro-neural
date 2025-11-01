param([int]$Port=8002)

$base = "http://127.0.0.1:$Port"

"==> HEALTH"
$h = Invoke-RestMethod "$base/health"
$h | Format-List
if ($h.status -ne "ok") { throw "Health falhou" }

$user = @'
{ "name":"Admin","email":"admin@mind.com","password":"123456","bio":"", "ai_profile":"" }
'@

try {
  "==> SIGNUP"
  Invoke-RestMethod "$base/users/" -Method POST -ContentType "application/json" -Body $user | Out-Null
} catch { "signup: pode já existir" }

$login = @'
{ "email":"admin@mind.com","password":"123456" }
'@

"==> LOGIN"
$tok = Invoke-RestMethod "$base/users/login" -Method POST -ContentType "application/json" -Body $login

$auth = @{ Authorization = "Bearer " + $tok.access_token }

"==> ME"
$me = Invoke-RestMethod "$base/users/me" -Headers $auth
$me | Format-List

if (-not $me.email) { throw "/users/me sem email" }

Write-Host "✅ Smoke OK"
