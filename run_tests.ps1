# Run tests and generate coverage report on Windows
# This script runs pytest with coverage analysis

Write-Host "🧪 Running tests with coverage analysis..." -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

# Run pytest with coverage
pytest test_main.py -v --cov=main --cov-report=term-missing --cov-report=html --cov-report=json

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Tests failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "✅ Tests passed! Coverage report generated." -ForegroundColor Green
Write-Host ""
Write-Host "📊 Coverage Reports Generated:" -ForegroundColor Cyan
Write-Host "  • Terminal report (above)" -ForegroundColor Yellow
Write-Host "  • HTML report: htmlcov/index.html" -ForegroundColor Yellow
Write-Host "  • JSON report: .coverage (can be viewed with coverage)" -ForegroundColor Yellow
Write-Host ""
Write-Host "📈 To view HTML report in browser:" -ForegroundColor Cyan
Write-Host "  Start-Process htmlcov/index.html" -ForegroundColor Yellow
