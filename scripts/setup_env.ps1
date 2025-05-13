# PowerShell script to set up .env and secrets for FormalAI project

param(
    [string]$EnvExamplePath = "../.env.example",
    [string]$EnvPath = "../.env"
)

Write-Host "=== FormalAI Environment Setup ===" -ForegroundColor Cyan

# Resolve paths relative to script location
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$envExample = Join-Path $scriptDir $EnvExamplePath
$envFile = Join-Path $scriptDir $EnvPath
$requirementsDevRoot = Join-Path $scriptDir "../requirements-dev.txt"
$requirementsRoot = Join-Path $scriptDir "../requirements.txt"
$requirementsDevClient = Join-Path $scriptDir "../src/client/python/requirements-dev.txt"
$requirementsClient = Join-Path $scriptDir "../src/client/python/requirements.txt"

# 1. Check for .env.example
if (!(Test-Path $envExample)) {
    Write-Host "ERROR: .env.example not found at $envExample" -ForegroundColor Red
    exit 1
}

# 2. Copy .env.example to .env if .env does not exist
if (!(Test-Path $envFile)) {
    Copy-Item $envExample $envFile
    Write-Host "Created .env from .env.example"
} else {
    Write-Host ".env already exists. Will update missing values only."
}

# 3. Parse .env.example for variable names
$exampleVars = Get-Content $envExample | Where-Object { $_ -match '^[A-Za-z_][A-Za-z0-9_]*=' } | ForEach-Object {
    ($_ -split '=',2)[0]
}

# 4. Load current .env values (if any)
$envVars = @{}
if (Test-Path $envFile) {
    Get-Content $envFile | Where-Object { $_ -match '^[A-Za-z_][A-Za-z0-9_]*=' } | ForEach-Object {
        $parts = $_ -split '=',2
        $envVars[$parts[0]] = $parts[1]
    }
}

# 5. Prompt for each variable
foreach ($var in $exampleVars) {
    $current = $envVars[$var]
    if ($current) {
        Write-Host "$var is already set in .env (value hidden)"
        continue
    }
    $value = Read-Host "Enter value for $var"
    Add-Content -Path $envFile -Value "$var=$value"
    Write-Host "Added $var to .env"
}

Write-Host "`n.env setup complete!" -ForegroundColor Green

# 6. Optionally install dependencies
$install = Read-Host "Install Python dependencies now? (y/n)"
if ($install -eq "y") {
    if (Test-Path $requirementsDevRoot) {
        Write-Host "Running: pip install -r $requirementsDevRoot"
        pip install -r $requirementsDevRoot
    } elseif (Test-Path $requirementsRoot) {
        Write-Host "Running: pip install -r $requirementsRoot"
        pip install -r $requirementsRoot
    } elseif (Test-Path $requirementsDevClient) {
        Write-Host "Running: pip install -r $requirementsDevClient"
        pip install -r $requirementsDevClient
    } elseif (Test-Path $requirementsClient) {
        Write-Host "Running: pip install -r $requirementsClient"
        pip install -r $requirementsClient
    } else {
        Write-Host "No requirements-dev.txt or requirements.txt found in project root or src/client/python/." -ForegroundColor Yellow
    }
}

Write-Host "`nAll done! You are ready to develop." -ForegroundColor Cyan
