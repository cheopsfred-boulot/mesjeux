param(
  [ValidateSet("loto", "euromillions", "crescendo")]
  [string]$FocusGame = "loto"
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$env:PYTHONPATH = "."

function Import-EnvFile {
  param(
    [Parameter(Mandatory = $true)]
    [string]$Path
  )

  if (-not (Test-Path -LiteralPath $Path)) {
    return
  }

  Get-Content -LiteralPath $Path | ForEach-Object {
    $line = $_.Trim()
    if (-not $line -or $line.StartsWith("#") -or -not $line.Contains("=")) {
      return
    }

    $parts = $line -split "=", 2
    $name = $parts[0].Trim()
    $value = $parts[1]
    if ($name) {
      Set-Item -Path "Env:$name" -Value $value
    }
  }
}

Import-EnvFile -Path (Join-Path $root ".env.local")
Import-EnvFile -Path (Join-Path $root ".env")

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
Invoke-PythonScript -Args @(
  "-c",
  "import json, sys; sys.path.insert(0, r'C:\projets\mesjeux'); from app.data_store import game_snapshot; print(json.dumps(game_snapshot('$FocusGame'), ensure_ascii=False))"
)
