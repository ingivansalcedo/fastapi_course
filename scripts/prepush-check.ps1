param(
    [switch]$SkipQuality,
    [switch]$SkipMigrations,
    [switch]$AutoFix
)

$ErrorActionPreference = "Stop"

function Write-Step {
    param([string]$Message)
    Write-Host ""
    Write-Host "==> $Message" -ForegroundColor Cyan
}

function Fail {
    param([string]$Message)
    Write-Host "ERROR: $Message" -ForegroundColor Red
    exit 1
}

$repoRoot = git rev-parse --show-toplevel 2>$null
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($repoRoot)) {
    Fail "No se detecto un repositorio Git valido."
}

Set-Location $repoRoot.Trim()

Write-Step "Estado general"
git status --short

Write-Step "Busqueda de secretos potenciales"
$secretFindings = @()

$urlFindings = git grep -nE "postgresql\+psycopg2://[^:@\s]+:[^@\s]+@" -- . ":(exclude).env.example" ":(exclude)README.md" 2>$null
if ($LASTEXITCODE -gt 1) {
    Fail "Fallo al ejecutar validacion de URL de base de datos."
}
if ($LASTEXITCODE -eq 0) {
    $secretFindings += $urlFindings
}

$envStyleFindings = git grep -nE "^(DB_PASSWORD|SECRET_KEY|API_KEY|TOKEN)=.+" -- . ":(exclude).env.example" ":(exclude)README.md" 2>$null
if ($LASTEXITCODE -gt 1) {
    Fail "Fallo al ejecutar validacion de variables sensibles."
}
if ($LASTEXITCODE -eq 0) {
    $secretFindings += $envStyleFindings
}

if ($secretFindings.Count -gt 0) {
    Write-Host "Se detectaron posibles secretos en archivos versionados:" -ForegroundColor Yellow
    $secretFindings | ForEach-Object { Write-Host $_ }
    Fail "Revisa y elimina esos valores antes de hacer push."
}

Write-Host "No se detectaron patrones de secretos en archivos versionados." -ForegroundColor Green

Write-Step "Verificacion de .gitignore"
$ignoreCheck = git check-ignore -v .env .env.example .venv/Scripts/python.exe 2>$null
if ($LASTEXITCODE -eq 0) {
    $ignoreCheck | ForEach-Object { Write-Host $_ }
} else {
    Write-Host "No se pudo validar todas las rutas de ejemplo. Revisa manualmente si es necesario." -ForegroundColor Yellow
}

if (-not $SkipQuality) {
    Write-Step "Validaciones de calidad"

    if ($AutoFix) {
        Write-Host "Modo AutoFix: aplicando correcciones automaticas de Ruff..." -ForegroundColor Yellow
        uv run ruff check . --fix
        if ($LASTEXITCODE -ne 0) {
            Fail "Ruff aplico correcciones parciales, pero quedaron problemas no auto-corregibles."
        }
    }

    uv run ruff check .
    if ($LASTEXITCODE -ne 0) {
        Fail "Ruff encontro problemas."
    }

    $maxPreCommitPasses = if ($AutoFix) { 5 } else { 1 }
    $preCommitPassed = $false

    for ($attempt = 1; $attempt -le $maxPreCommitPasses; $attempt++) {
        uv run pre-commit run --all-files
        if ($LASTEXITCODE -eq 0) {
            $preCommitPassed = $true
            break
        }

        if ($attempt -lt $maxPreCommitPasses) {
            Write-Host "pre-commit aplico cambios o reporto issues. Reintentando ($attempt/$maxPreCommitPasses)..." -ForegroundColor Yellow
        }
    }

    if (-not $preCommitPassed) {
        Fail "pre-commit encontro problemas."
    }
} else {
    Write-Host ""
    Write-Host "==> Validaciones de calidad omitidas por parametro" -ForegroundColor Yellow
}

if (-not $SkipMigrations) {
    Write-Step "Estado de migraciones"
    uv run db-current
    if ($LASTEXITCODE -ne 0) {
        Fail "No se pudo obtener db-current."
    }

    uv run db-history
    if ($LASTEXITCODE -ne 0) {
        Fail "No se pudo obtener db-history."
    }
} else {
    Write-Host ""
    Write-Host "==> Validaciones de migracion omitidas por parametro" -ForegroundColor Yellow
}

Write-Step "Revision de cambios staged"
git diff --staged

Write-Host ""
Write-Host "Checklist pre-push completado correctamente." -ForegroundColor Green
Write-Host 'Si todo esta correcto: git add . ; git commit -m "mensaje" ; git push'
