<#
.SYNOPSIS
    Configura o ambiente virtual Python de forma mandatoria para o workspace All-in-One.
#>
$ErrorActionPreference = "Stop"

Write-Host "Iniciando configuracao persistente do ambiente Python..." -ForegroundColor Cyan

if (-not (Test-Path ".venv")) {
    Write-Host "Criando diretorio .venv..."
    python -m venv .venv
}

Write-Host "Atualizando pip e dependencias essenciais..."
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt

if (-not (Test-Path ".vscode\settings.json")) {
    throw "Configuracao obrigatoria ausente: .vscode\settings.json"
}

$settings = Get-Content ".vscode\settings.json" -Raw | ConvertFrom-Json
$expectedInterpreter = 'C:\Users\ereta\.codex\worktrees\all-in-one\.venv\Scripts\python.exe'
if ($settings.'python.defaultInterpreterPath' -ne $expectedInterpreter) {
    throw "python.defaultInterpreterPath deve ser $expectedInterpreter"
}

Write-Host "Ambiente resolvido com sucesso para $expectedInterpreter" -ForegroundColor Green
