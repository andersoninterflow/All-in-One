# Script para fazer tag e push de todas as imagens All-in-One para Docker Hub
# Uso: .\scripts\docker_tag_and_push.ps1 -Username "andersoninterflow"

param(
    [string]$Username = "andersoninterflow",
    [string]$Tag = "latest"
)

$modules = @(
    "api-hub",
    "identity",
    "finance",
    "marketplace",
    "delivery",
    "services",
    "mobility",
    "erp",
    "wms",
    "tms",
    "crm",
    "health",
    "jobs",
    "outbox-dispatcher",
    "retention-worker"
)

Write-Host "🐳 Iniciando tagging e push para Docker Hub ($Username)" -ForegroundColor Cyan
Write-Host "Tag: $Tag`n" -ForegroundColor Yellow

$successCount = 0
$failedCount = 0
$failedModules = @()

foreach ($module in $modules) {
    $imageName = "all-in-one-$module"
    $hubName = "$Username/all-in-one-$module"
    $fullTag = "$hubName`:$Tag"
    
    Write-Host "📦 Processando: $module" -ForegroundColor White
    
    # Verificar se a imagem existe localmente
    $imageExists = docker images --quiet "$imageName" 2>$null
    if (-not $imageExists) {
        Write-Host "   ❌ Imagem não encontrada: $imageName" -ForegroundColor Red
        $failedCount++
        $failedModules += $module
        continue
    }
    
    # Fazer tag
    Write-Host "   🏷️  Fazendo tag para: $fullTag" -ForegroundColor Gray
    docker tag "$imageName" "$fullTag" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ Tag criada com sucesso" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Erro ao criar tag" -ForegroundColor Red
        $failedCount++
        $failedModules += $module
        continue
    }
    
    # Fazer push
    Write-Host "   📤 Enviando para Docker Hub..." -ForegroundColor Gray
    docker push "$fullTag" 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ Push realizado com sucesso" -ForegroundColor Green
        $successCount++
    } else {
        Write-Host "   ❌ Erro ao fazer push" -ForegroundColor Red
        $failedCount++
        $failedModules += $module
    }
    
    Write-Host ""
}

Write-Host "`n" + ("="*60) -ForegroundColor Cyan
Write-Host "📊 RESULTADO FINAL" -ForegroundColor Cyan
Write-Host ("="*60) -ForegroundColor Cyan
Write-Host "✅ Sucesso: $successCount" -ForegroundColor Green
Write-Host "❌ Falhas: $failedCount" -ForegroundColor Red

if ($failedCount -gt 0) {
    Write-Host "`nMódulos com falha:" -ForegroundColor Yellow
    foreach ($failed in $failedModules) {
        Write-Host "  - $failed" -ForegroundColor Red
    }
}

Write-Host "`n🔗 Repositório: https://hub.docker.com/u/$Username" -ForegroundColor Blue
Write-Host ""
