param(
    [switch]$SkipWinget,
    [switch]$SkipVsCodeExtensions,
    [switch]$SkipPythonDeps
)

$ErrorActionPreference = "Stop"

function Add-UserPathEntry {
    param([string]$PathEntry)

    if ([string]::IsNullOrWhiteSpace($PathEntry) -or -not (Test-Path $PathEntry)) {
        return
    }

    $currentUserPath = [Environment]::GetEnvironmentVariable("Path", "User")
    $items = @()
    if (-not [string]::IsNullOrWhiteSpace($currentUserPath)) {
        $items = $currentUserPath -split ";" | Where-Object { -not [string]::IsNullOrWhiteSpace($_) }
    }

    if ($items -notcontains $PathEntry) {
        $items += $PathEntry
        [Environment]::SetEnvironmentVariable("Path", ($items -join ";"), "User")
        Write-Host "PATH de usuario atualizado: $PathEntry"
    }

    $processItems = $env:Path -split ";" | Where-Object { -not [string]::IsNullOrWhiteSpace($_) }
    if ($processItems -notcontains $PathEntry) {
        $env:Path = (($processItems + $PathEntry) -join ";")
    }
}

function Resolve-CommandPath {
    param(
        [string]$CommandName,
        [string[]]$Candidates = @()
    )

    $command = Get-Command $CommandName -ErrorAction SilentlyContinue
    if ($command) {
        return $command.Source
    }

    foreach ($candidate in $Candidates) {
        if (Test-Path $candidate) {
            return $candidate
        }
    }

    return $null
}

function Invoke-Optional {
    param(
        [string]$Executable,
        [string[]]$Arguments
    )

    & $Executable @Arguments
    $exitCode = 0
    if ($null -ne $LASTEXITCODE) {
        $exitCode = $LASTEXITCODE
    }
    if ($exitCode -ne 0) {
        Write-Warning "$Executable $($Arguments -join ' ') retornou codigo $exitCode"
    }
}

function Install-WingetPackage {
    param(
        [string]$Winget,
        [string]$Id,
        [string]$Name
    )

    Write-Host "Verificando pacote: $Name ($Id)"
    & $Winget list --id $Id --exact --accept-source-agreements *> $null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Ja instalado: $Name"
        return
    }

    Write-Host "Instalando: $Name"
    Invoke-Optional $Winget @(
        "install",
        "--id", $Id,
        "--exact",
        "--silent",
        "--accept-package-agreements",
        "--accept-source-agreements"
    )
}

$git = Resolve-CommandPath "git" @(
    "C:\Program Files\Git\cmd\git.exe",
    "C:\Program Files\Git\bin\git.exe",
    "$env:LOCALAPPDATA\Programs\Git\cmd\git.exe",
    "$env:LOCALAPPDATA\Programs\Git\bin\git.exe"
)

$repoRoot = $null
if ($git) {
    $repoRoot = (& $git rev-parse --show-toplevel 2>$null)
}
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($repoRoot)) {
    $repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
}
Set-Location $repoRoot

$localAppData = [Environment]::GetFolderPath("LocalApplicationData")
$userProfile = [Environment]::GetFolderPath("UserProfile")

$pathEntries = @(
    "C:\Program Files\Git\cmd",
    "C:\Program Files\Git\bin",
    "C:\Program Files\PowerShell\7",
    "C:\Program Files\Docker\Docker\resources\bin",
    (Join-Path $localAppData "Programs\Microsoft VS Code\bin"),
    (Join-Path $localAppData "Microsoft\WindowsApps"),
    (Join-Path $userProfile ".local\bin")
)

foreach ($entry in $pathEntries) {
    Add-UserPathEntry $entry
}

$winget = Resolve-CommandPath "winget" @(
    (Join-Path $localAppData "Microsoft\WindowsApps\winget.exe")
)

if (-not $SkipWinget) {
    if ($winget) {
        $packages = @(
            @{ Id = "Git.Git"; Name = "Git for Windows" },
            @{ Id = "Microsoft.PowerShell"; Name = "PowerShell 7" },
            @{ Id = "Docker.DockerDesktop"; Name = "Docker Desktop" },
            @{ Id = "Python.Python.3.12"; Name = "Python 3.12" },
            @{ Id = "OpenJS.NodeJS.LTS"; Name = "Node.js LTS" },
            @{ Id = "GitHub.cli"; Name = "GitHub CLI" },
            @{ Id = "Microsoft.VisualStudioCode"; Name = "Visual Studio Code" }
        )

        foreach ($package in $packages) {
            Install-WingetPackage $winget $package.Id $package.Name
        }
    } else {
        Write-Warning "winget nao encontrado; instalacao automatica de pacotes Windows foi ignorada."
    }
}

if (-not $SkipVsCodeExtensions) {
    $code = Resolve-CommandPath "code" @(
        (Join-Path $localAppData "Programs\Microsoft VS Code\bin\code.cmd")
    )

    if ($code) {
        $extensions = @(
            "ms-python.python",
            "ms-python.vscode-pylance",
            "ms-python.debugpy",
            "ms-azuretools.vscode-docker",
            "ms-vscode.powershell",
            "redhat.vscode-yaml",
            "github.vscode-github-actions",
            "github.vscode-pull-request-github",
            "eamodio.gitlens",
            "ms-vscode-remote.remote-wsl",
            "ms-kubernetes-tools.vscode-kubernetes-tools"
        )

        foreach ($extension in $extensions) {
            Write-Host "Instalando/extensao VS Code: $extension"
            Invoke-Optional $code @("--install-extension", $extension, "--force")
        }
    } else {
        Write-Warning "VS Code CLI nao encontrado; extensoes nao foram instaladas automaticamente."
    }
}

if (-not $SkipPythonDeps) {
    $python = Join-Path $repoRoot ".venv\Scripts\python.exe"
    if (-not (Test-Path $python)) {
        $python = Resolve-CommandPath "python" @()
    }

    if ($python) {
        Invoke-Optional $python @("-m", "pip", "install", "--upgrade", "pip")
        $requirementFiles = @("requirements-dev.txt")
        $requirementFiles += Get-ChildItem -Path "modules", "workers" -Filter "requirements.txt" -Recurse -ErrorAction SilentlyContinue |
            ForEach-Object { $_.FullName }

        foreach ($requirements in $requirementFiles) {
            if (Test-Path $requirements) {
                Write-Host "Instalando dependencias Python: $requirements"
                Invoke-Optional $python @("-m", "pip", "install", "-r", $requirements)
            }
        }
    } else {
        Write-Warning "Python nao encontrado; dependencias Python nao foram instaladas."
    }
}

Write-Host "Bootstrap concluido. Abra um novo terminal para herdar o PATH persistente."
