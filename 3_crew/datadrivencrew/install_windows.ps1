# Windows Installation Fix Script for chroma-hnswlib
# This script fixes the Microsoft Visual C++ build tools issue by pre-installing
# the Windows wheel for chroma-hnswlib before installing other dependencies.

Write-Host "Checking Python version..." -ForegroundColor Cyan
$pythonVersion = python --version 2>&1
Write-Host "Python version: $pythonVersion" -ForegroundColor Green

# Check if Python version is 3.10, 3.11, or 3.12 (wheels are available for these)
$pythonVersionMatch = $pythonVersion -match "Python (\d+)\.(\d+)"
if ($pythonVersionMatch) {
    $majorVersion = [int]$matches[1]
    $minorVersion = [int]$matches[2]
    
    if ($majorVersion -eq 3 -and ($minorVersion -ge 10 -and $minorVersion -le 12)) {
        Write-Host "Python version is compatible. Installing chroma-hnswlib wheel..." -ForegroundColor Green
        
        # Pre-install chroma-hnswlib using the wheel (no compilation needed)
        Write-Host "Installing chroma-hnswlib (pre-built wheel)..." -ForegroundColor Cyan
        python -m pip install --only-binary :all: chroma-hnswlib==0.7.6
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Successfully installed chroma-hnswlib wheel!" -ForegroundColor Green
            Write-Host "Now you can proceed with: crewai install" -ForegroundColor Cyan
        } else {
            Write-Host "Failed to install chroma-hnswlib wheel. Trying alternative method..." -ForegroundColor Yellow
            python -m pip install chroma-hnswlib==0.7.6 --only-binary=:all:
        }
    } else {
        Write-Host "Warning: Python version $majorVersion.$minorVersion may not have pre-built wheels." -ForegroundColor Yellow
        Write-Host "Pre-built wheels are available for Python 3.10, 3.11, and 3.12." -ForegroundColor Yellow
        Write-Host "Attempting to install anyway..." -ForegroundColor Cyan
        python -m pip install --only-binary :all: chroma-hnswlib==0.7.6
    }
} else {
    Write-Host "Could not determine Python version. Attempting installation anyway..." -ForegroundColor Yellow
    python -m pip install --only-binary :all: chroma-hnswlib==0.7.6
}

Write-Host "`nInstallation fix complete!" -ForegroundColor Green
Write-Host "You can now run: crewai install" -ForegroundColor Cyan

