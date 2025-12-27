param([int]$Port=8000)
Set-Location $PSScriptRoot\..\
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port $Port --reload
