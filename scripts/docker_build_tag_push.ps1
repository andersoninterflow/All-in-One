# Script completo: Build + Tag + Push para Docker Hub
# Uso: .\scripts\docker_build_tag_push.ps1 -Username "andersoninterflow"

param(
    [string]$Username = "andersoninterflow",
    [string]$Tag = "latest",
    [int]$MaxWaitMinutes = 30
)

$ErrorActionPreference = "Continue"
$projectRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$composeFile = "$projectRoot\infra\docker\docker-compose.yml"

Write-Host "🚀 All-in-One: Build → Tag → Push" -ForegroundColor Cyan
Write-Host "Projeto: $projectRoot" -ForegroundColor Gray
Write-Host "Compose: $composeFile" -ForegroundColor Gray
Write-Host ""

# Passo 1: Construir imagens
Write-Host "📦 Passo 1: Construindo imagens Docker..." -ForegroundColor Yellow
Write-Host "Aguardando (máximo $MaxWaitMinutes minutos)..." -ForegroundColor Gray

$startTime = Get-Date
$buildProcess = Start-Process -FilePath "docker" -ArgumentList "compose", "-f", $composeFile, "build" -NoNewWindow -PassThru

$timeout = $MaxWaitMinutes * 60
while (-not $buildProcess.HasExited) {
    $elapsedSeconds = ([DateTime]::Now - $startTime).TotalSeconds
    if ($elapsedSeconds -gt $timeout) {
        Write-Host "⏱️  Timeout atingido ($MaxWaitMinutes min). Continuando com imagens existentes..." -ForegroundColor Yellow
        $buildProcess.Kill()
        break
    }
    Start-Sleep -Seconds 5
    Write-Host "⏳ Construindo... ($([int]($elapsedSeconds / 60))m $([int]($elapsedSeconds % 60))s)" -ForegroundColor Gray
}

if ($buildProcess.HasExited -and $buildProcess.ExitCode -eq 0) {
    Write-Host "✅ Build concluído com sucesso`n" -ForegroundColor Green
} else {
    Write-Host "⚠️  Build em andamento ou com problemas. Continuando com o tagging...`n" -ForegroundColor Yellow
}

# Passo 2: Listar imagens construídas
Write-Host "📋 Passo 2: Listando imagens all-in-one..." -ForegroundColor Yellow
$images = docker images --filter "reference=all-in-one*" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
Write-Host $images
Write-Host ""

# Passo 3: Fazer tag de cada imagem
Write-Host "🏷️  Passo 3: Fazendo tag das imagens..." -ForegroundColor Yellow
$taggedCount = 0
docker images --filter "reference=all-in-one*" --format "{{.Repository}}" | ForEach-Object {
    $localImage = $_
    $imageName = $localImage -replace "all-in-one-", ""
    $remoteImage = "$Username/all-in-one-$imageName"
    
    Write-Host "  Tagging: $localImage → $remoteImage" -ForegroundColor Gray
    docker tag "$localImage" "$remoteImage`:$Tag" 2>$null
    if ($?) {
        Write-Host "  ✅ OK" -ForegroundColor Green
        $taggedCount++
    } else {
        Write-Host "  ❌ Erro" -ForegroundColor Red
    }
}
Write-Host "✅ $taggedCount imagens tagueadas`n" -ForegroundColor Green

# Passo 4: Fazer push para Docker Hub
Write-Host "📤 Passo 4: Enviando imagens para Docker Hub..." -ForegroundColor Yellow
Write-Host "Repositório: $Username" -ForegroundColor Gray
Write-Host ""

$pushedCount = 0
docker images --filter "reference=$Username/all-in-one*" --format "{{.Repository}}:{{.Tag}}" | ForEach-Object {
    $image = $_
    $shortName = $image -replace "$Username/all-in-one-", "" -replace ":$Tag", ""
    
    Write-Host "  📤 Enviando: $shortName" -ForegroundColor Cyan
    docker push "$image" 2>&1 | Select-String -Pattern "Pushed|latest|digest" | ForEach-Object { Write-Host "     $_" -ForegroundColor Gray }
    
    if ($?) {
        Write-Host "  ✅ OK`n" -ForegroundColor Green
        $pushedCount++
    } else {
        Write-Host "  ❌ Erro`n" -ForegroundColor Red
    }
}

# Resumo final
Write-Host "`n" + ("="*70) -ForegroundColor Cyan
Write-Host "✨ CONCLUÍDO" -ForegroundColor Cyan
Write-Host ("="*70) -ForegroundColor Cyan
Write-Host "✅ Imagens construídas: $(docker images --filter 'reference=all-in-one*' --format 'table' | wc -l)" -ForegroundColor Green
Write-Host "✅ Imagens tagueadas: $taggedCount" -ForegroundColor Green
Write-Host "✅ Imagens enviadas: $pushedCount" -ForegroundColor Green
Write-Host ""
Write-Host "🔗 Seu repositório: https://hub.docker.com/u/$Username" -ForegroundColor Blue
Write-Host "📌 Próximos passos:" -ForegroundColor Yellow
Write-Host "   1. Verificar imagens: https://hub.docker.com/u/$Username/repositories" -ForegroundColor Gray
Write-Host "   2. Testar pull: docker pull $Username/all-in-one-api-hub:$Tag" -ForegroundColor Gray
Write-Host ""
