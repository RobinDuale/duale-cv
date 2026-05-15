# preview-worktree.ps1
# Lance un serveur local sur http://localhost:3457 depuis le worktree Claude le plus recent
# Usage : .\preview-worktree.ps1
# Arret : Ctrl+C

$PORT = 3457
$worktreesRoot = Join-Path $PSScriptRoot ".claude\worktrees"

if (-not (Test-Path $worktreesRoot)) {
    Write-Host "Aucun worktree trouve dans .claude\worktrees\"
    exit 1
}

# Libere le port si un process l'occupe encore
$existing = netstat -ano | Select-String ":$PORT\s" | ForEach-Object {
    ($_ -split '\s+')[-1]
} | Select-Object -Unique
foreach ($pid in $existing) {
    if ($pid -match '^\d+$') {
        Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
        Write-Host "Process $pid libere sur le port $PORT"
    }
}

# Prend le worktree modifie le plus recemment
$worktreePath = Get-ChildItem -Path $worktreesRoot -Directory |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1 -ExpandProperty FullName

if ($worktreePath) {
    Write-Host "Worktree : $worktreePath"
    Write-Host "Preview  : http://localhost:$PORT/fr/"
    Write-Host "Arret    : Ctrl+C"
    Write-Host ""
    Set-Location $worktreePath
    python -m http.server $PORT
} else {
    Write-Host "Aucun worktree actif trouve. Lance d'abord une session Claude Code."
}
