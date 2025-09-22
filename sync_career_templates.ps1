# Career Template Synchronization Script (PowerShell)
# This script automates the process of keeping career templates up-to-date
# by extracting career types, finding missing templates, and generating placeholders.

# Set error action preference to stop on errors
$ErrorActionPreference = "Stop"

Write-Host "🚀 Starting Career Template Synchronization Process..." -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green

try {
    # Step 1: Extract career types from the backend
    Write-Host "📊 Step 1: Extracting career types from backend..." -ForegroundColor Yellow
    python extract_career_types.py
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Career types extracted successfully" -ForegroundColor Green
    } else {
        throw "Failed to extract career types"
    }

    Write-Host ""

    # Step 2: Find missing templates by comparing extracted types with existing templates
    Write-Host "🔍 Step 2: Finding missing career templates..." -ForegroundColor Yellow
    Set-Location scripts
    npx ts-node find_missing_templates.ts
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Missing templates identified successfully" -ForegroundColor Green
    } else {
        throw "Failed to identify missing templates"
    }

    Write-Host ""

    # Step 3: Generate placeholder templates for any missing career types
    Write-Host "🏗️  Step 3: Generating placeholder templates..." -ForegroundColor Yellow
    npx ts-node generate_placeholder_templates.ts
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Placeholder templates generated successfully" -ForegroundColor Green
    } else {
        throw "Failed to generate placeholder templates"
    }

    # Return to root directory
    Set-Location ..

    Write-Host ""
    Write-Host "🎉 Career Template Synchronization Complete!" -ForegroundColor Green
    Write-Host "=============================================" -ForegroundColor Green
    Write-Host "All career templates are now up-to-date." -ForegroundColor White
    Write-Host ""
    Write-Host "Summary of actions performed:" -ForegroundColor White
    Write-Host "1. ✅ Extracted latest career types from backend" -ForegroundColor Green
    Write-Host "2. ✅ Identified missing career templates" -ForegroundColor Green
    Write-Host "3. ✅ Generated placeholder templates for missing careers" -ForegroundColor Green
    Write-Host ""
    Write-Host "You can now review the generated templates and customize them as needed." -ForegroundColor White

} catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    Set-Location .. # Ensure we return to root directory even on error
    exit 1
}