param(
    [string]$CodexRoot
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

if ([string]::IsNullOrWhiteSpace($CodexRoot)) {
    if (-not [string]::IsNullOrWhiteSpace($env:CODEX_HOME)) {
        $CodexRoot = $env:CODEX_HOME
    } else {
        $CodexRoot = Join-Path $HOME ".codex"
    }
}

$PetDir = Join-Path (Join-Path $CodexRoot "pets") "sanhao-tu"
New-Item -ItemType Directory -Force -Path $PetDir | Out-Null
Copy-Item -Force (Join-Path $ScriptDir "pet.json") (Join-Path $PetDir "pet.json")
Copy-Item -Force (Join-Path $ScriptDir "spritesheet.webp") (Join-Path $PetDir "spritesheet.webp")

Write-Host "三好兔已经安装到：$PetDir"
Write-Host "重新启动 Codex，或在宠物选择器中重新选择三好兔。"
