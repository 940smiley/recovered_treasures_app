param([int]$Port=5173)
Set-Location $PSScriptRoot
python -m http.server $Port
