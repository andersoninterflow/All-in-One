param(
    [string]$Branch = "",
    [string[]]$Remotes = @("origin", "fork"),
    [switch]$AllowAhead,
    [switch]$AllowDirty,
    [switch]$NoFetch
)

$ErrorActionPreference = "Stop"

function Invoke-Git {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$GitArgs)
    $output = & git @GitArgs 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "git $($GitArgs -join ' ') falhou: $output"
    }
    return $output
}

function Test-GitPath {
    param([string]$Path)
    $value = (& git rev-parse --git-path $Path).Trim()
    if ($LASTEXITCODE -ne 0) {
        throw "Nao foi possivel resolver caminho Git: $Path"
    }
    return (Test-Path $value)
}

$repoRoot = (& git rev-parse --show-toplevel).Trim()
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($repoRoot)) {
    throw "Este comando precisa ser executado dentro de um repositorio Git."
}
Set-Location $repoRoot

if ((Test-GitPath "MERGE_HEAD") -or (Test-GitPath "rebase-merge") -or (Test-GitPath "rebase-apply")) {
    throw "Verificacao bloqueada: ha merge ou rebase em andamento."
}

if ([string]::IsNullOrWhiteSpace($Branch)) {
    $Branch = (& git branch --show-current).Trim()
    if ([string]::IsNullOrWhiteSpace($Branch) -and $env:GITHUB_REF_NAME) {
        $Branch = $env:GITHUB_REF_NAME
    }
    if ([string]::IsNullOrWhiteSpace($Branch)) {
        throw "Nao foi possivel identificar a branch atual. Informe -Branch."
    }
}

$status = (& git status --porcelain)
if ($status -and -not $AllowDirty) {
    throw "A arvore de trabalho possui alteracoes locais. Use -AllowDirty apenas para diagnostico."
}

$availableRemotes = @(& git remote)
$checked = 0
$problems = New-Object System.Collections.Generic.List[string]

foreach ($remote in $Remotes) {
    if ($availableRemotes -notcontains $remote) {
        Write-Warning "Remoto ausente neste checkout: $remote"
        continue
    }

    if (-not $NoFetch) {
        & git fetch $remote $Branch --prune | Out-Host
        if ($LASTEXITCODE -ne 0) {
            $problems.Add("Fetch falhou para $remote/$Branch.")
            continue
        }
    }

    & git rev-parse --verify "$remote/$Branch" *> $null
    if ($LASTEXITCODE -ne 0) {
        $problems.Add("Referencia remota inexistente: $remote/$Branch.")
        continue
    }

    $counts = (& git rev-list --left-right --count "$remote/$Branch...HEAD").Trim() -split "\s+"
    $behind = [int]$counts[0]
    $ahead = [int]$counts[1]
    $checked += 1

    if ($behind -gt 0) {
        $problems.Add("Branch local esta $behind commit(s) atras de $remote/$Branch.")
    }
    if ($ahead -gt 0 -and -not $AllowAhead) {
        $problems.Add("Branch local esta $ahead commit(s) a frente de $remote/$Branch.")
    }

    Write-Host "$remote/$Branch: behind=$behind ahead=$ahead"
}

if ($checked -eq 0) {
    throw "Nenhum remoto verificavel encontrado para a branch $Branch."
}

if ($problems.Count -gt 0) {
    throw "Divergencia Git detectada:`n- $($problems -join "`n- ")"
}

Write-Host "Sincronizacao Git validada para $checked remoto(s)."
