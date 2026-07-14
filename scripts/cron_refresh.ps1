param(
  [ValidateSet("loto", "euromillions", "crescendo")]
  [string]$FocusGame = "loto"
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$env:PYTHONPATH = "."

function Invoke-PythonScript {
  param(
    [Parameter(Mandatory = $true)]
    [string[]]$Args
  )

  & python @Args
  if ($LASTEXITCODE -ne 0) {
    throw "Python command failed: python $($Args -join ' ')"
  }
}

Invoke-PythonScript -Args @("scripts\refresh_all.py")
Invoke-PythonScript -Args @("scripts\sync_neon.py")
Invoke-PythonScript -Args @("scripts\export_csv.py", "--all")
Invoke-PythonScript -Args @(
  "-c",
  "import json, sys; sys.path.insert(0, r'C:\projets\mesjeux'); from app.data_store import game_snapshot; print(json.dumps(game_snapshot('$FocusGame'), ensure_ascii=False))"
)
