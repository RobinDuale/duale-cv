# preview-worktree.ps1
# Lance un serveur local sur http://localhost:3457 depuis le worktree Claude actif
# Usage : .\preview-worktree.ps1

$worktreePath = git worktree list 2>$null |
    Where-Object { $_ -match '\.claude[\\/]worktrees[\\/]' } |
    ForEach-Object { ($_ -split '\s+')[0] } |
    Select-Object -Last 1

if ($worktreePath -and (Test-Path $worktreePath)) {
    Write-Host "Worktree : $worktreePath"
    Write-Host "Preview  : http://localhost:3457/fr/"
    Write-Host ""
    Set-Location $worktreePath
    npx serve . -p 3457 --no-clipboard
} else {
    Write-Host "Aucun worktree actif trouve. Lance d'abord une session Claude Code."
}
