param(
    [string]$ComposeFile = "infra/docker/docker-compose.yml",
    [int]$TimeoutSeconds = 240,
    [switch]$SkipBuild,
    [switch]$DownAfter
)

$ErrorActionPreference = "Stop"

function Invoke-Checked {
    param(
        [string]$Command,
        [string[]]$Arguments
    )
    & $Command @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "$Command $($Arguments -join ' ') falhou com codigo $LASTEXITCODE"
    }
}

$repoRoot = (& git rev-parse --show-toplevel).Trim()
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($repoRoot)) {
    throw "Este comando precisa ser executado dentro de um repositorio Git."
}
Set-Location $repoRoot

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw "Docker nao encontrado no PATH."
}

if (-not (Test-Path $ComposeFile)) {
    throw "Arquivo compose nao encontrado: $ComposeFile"
}

$compose = @("compose", "-f", $ComposeFile)
$services = @(
    @{ Name = "api-hub"; Port = 8100 },
    @{ Name = "identity"; Port = 8101 },
    @{ Name = "finance"; Port = 8102 },
    @{ Name = "marketplace"; Port = 8103 },
    @{ Name = "delivery"; Port = 8104 },
    @{ Name = "services"; Port = 8105 },
    @{ Name = "mobility"; Port = 8106 },
    @{ Name = "erp"; Port = 8107 },
    @{ Name = "wms"; Port = 8108 },
    @{ Name = "tms"; Port = 8109 },
    @{ Name = "crm"; Port = 8110 },
    @{ Name = "health"; Port = 8111 },
    @{ Name = "jobs"; Port = 8112 }
)

try {
    Invoke-Checked docker ($compose + @("config", "--quiet"))

    $upArgs = $compose + @("up", "-d")
    if (-not $SkipBuild) {
        $upArgs += "--build"
    }
    Invoke-Checked docker $upArgs

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    $pending = [System.Collections.Generic.HashSet[string]]::new()
    foreach ($service in $services) {
        [void]$pending.Add($service.Name)
    }

    while ($pending.Count -gt 0 -and (Get-Date) -lt $deadline) {
        foreach ($service in $services) {
            if (-not $pending.Contains($service.Name)) {
                continue
            }
            $url = "http://127.0.0.1:$($service.Port)/health"
            try {
                $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 3
                if ($response.StatusCode -ge 200 -and $response.StatusCode -lt 300 -and $response.Content -match "ok") {
                    Write-Host "$($service.Name) healthy em $url"
                    [void]$pending.Remove($service.Name)
                }
            } catch {
                Start-Sleep -Seconds 1
            }
        }
    }

    if ($pending.Count -gt 0) {
        Invoke-Checked docker ($compose + @("ps"))
        throw "Servicos sem health HTTP dentro de $TimeoutSeconds segundo(s): $($pending -join ', ')"
    }

    Write-Host "Docker Compose validado: $($services.Count) APIs FastAPI healthy."
} finally {
    if ($DownAfter) {
        & docker @($compose + @("down", "--remove-orphans"))
    }
}
