param(
  [string]$FocusGame = "loto"
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$env:PYTHONPATH = "."

function Resolve-Python {
  if ($env:PYTHON_EXE -and (Test-Path -LiteralPath $env:PYTHON_EXE)) {
    return $env:PYTHON_EXE
  }

  $fallback = "C:\projets\python313\python.exe"
  if (Test-Path -LiteralPath $fallback) {
    return $fallback
  }

  $cmd = Get-Command python -ErrorAction SilentlyContinue
  if ($cmd -and $cmd.Source) {
    return $cmd.Source
  }

  $py = Get-Command py -ErrorAction SilentlyContinue
  if ($py -and $py.Source) {
    return $py.Source
  }

  throw "Unable to locate a Python executable. Set PYTHON_EXE in .env.local."
}

function Resolve-FocusGame {
  param(
    [Parameter(Mandatory = $true)]
    [string]$Value
  )

  switch ($Value.ToLowerInvariant()) {
    "loto" { return "loto" }
    "euromillion" { return "euromillions" }
    "euromillions" { return "euromillions" }
    "crescendo" { return "crescendo" }
    "crecndo" { return "crescendo" }
    "cresendo" { return "crescendo" }
    default {
      throw "Unsupported FocusGame '$Value'. Use loto, euromillions, or crescendo."
    }
  }
}

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

$FocusGame = Resolve-FocusGame -Value $FocusGame

Import-EnvFile -Path (Join-Path $root ".env.local")
Import-EnvFile -Path (Join-Path $root ".env")

function Invoke-PythonScript {
  param(
    [Parameter(Mandatory = $true)]
    [string[]]$Args
  )

  $pythonExe = Resolve-Python
  & $pythonExe @Args
  if ($LASTEXITCODE -ne 0) {
    throw "Python command failed: $pythonExe $($Args -join ' ')"
  }
}

Invoke-PythonScript -Args @("scripts\refresh_all.py")
Invoke-PythonScript -Args @("scripts\sync_neon.py")
Invoke-PythonScript -Args @(
  "-c",
  "import json, sys; sys.path.insert(0, r'C:\projets\mesjeux'); from app.data_store import game_snapshot; print(json.dumps(game_snapshot('$FocusGame'), ensure_ascii=False))"
)
