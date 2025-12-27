# One-click launcher for Seller Dashboard (backend + frontend)
param([int]$ApiPort=8000, [int]$WebPort=5173)

function Get-LanIP {
  $ip = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "Ethernet*","Wi-Fi*" -ErrorAction SilentlyContinue | Where-Object {$_.IPAddress -notlike "169.254*" -and $_.IPAddress -ne "127.0.0.1"} | Select-Object -First 1 -ExpandProperty IPAddress)
  if (-not $ip) { $ip = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -notlike "169.254*" -and $_.IPAddress -ne "127.0.0.1"} | Select-Object -First 1 -ExpandProperty IPAddress) }
  return $ip
}

Write-Host "== Starting Seller Dashboard ==" -ForegroundColor Cyan

# Start backend
Push-Location "$root\backend"
if (-not (Test-Path .venv)) { python -m venv .venv }
. .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt | Out-Null

$backendCmd = "uvicorn app.main:app --host 0.0.0.0 --port $ApiPort --reload"
Start-Process -WindowStyle Minimized powershell -ArgumentList "-NoLogo","-NoProfile","-Command",$backendCmd
Pop-Location

# Start frontend
Push-Location "$root\frontend"
$frontendCmd = "python -m http.server $WebPort"
Start-Process -WindowStyle Minimized powershell -ArgumentList "-NoLogo","-NoProfile","-Command",$frontendCmd
Pop-Location

Start-Sleep -Seconds 2

$lan = Get-LanIP
Write-Host "Backend:  http://localhost:$ApiPort    (LAN: http://$lan:$ApiPort)"
Write-Host "Frontend: http://localhost:$WebPort  (LAN: http://$lan:$WebPort)" -ForegroundColor Green
Write-Host "Tip: Open the LAN Frontend URL on your iPhone and Add to Home Screen."

# Auto-open browser to local frontend
Start-Sleep -Seconds 1
Start-Process "http://localhost:"
