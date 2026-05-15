# preview-worktree.ps1
# Lance un serveur local sur http://localhost:3457 depuis le worktree Claude le plus recent
# Usage : .\preview-worktree.ps1

$worktreesRoot = Join-Path $PSScriptRoot ".claude\worktrees"

if (-not (Test-Path $worktreesRoot)) {
    Write-Host "Aucun worktree trouve dans .claude\worktrees\"
    exit 1
}

# Prend le worktree modifie le plus recemment
$worktreePath = Get-ChildItem -Path $worktreesRoot -Directory |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1 -ExpandProperty FullName

if ($worktreePath) {
    Write-Host "Worktree : $worktreePath"
    Write-Host "Preview  : http://localhost:3457/fr/"
    Write-Host ""
    Set-Location $worktreePath
    npx serve . -p 3457 --no-clipboard
} else {
    Write-Host "Aucun worktree actif trouve. Lance d'abord une session Claude Code."
}
