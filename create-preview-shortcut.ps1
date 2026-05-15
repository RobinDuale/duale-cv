# create-preview-shortcut.ps1
# Cree un raccourci "Preview Site" sur le Bureau
# A lancer une seule fois. Le raccourci peut ensuite etre epingle a la barre des taches.

$scriptPath = Join-Path $PSScriptRoot "preview-worktree.ps1"
$shortcutPath = Join-Path ([Environment]::GetFolderPath("Desktop")) "Preview Site.lnk"

$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = "powershell.exe"
$shortcut.Arguments = "-NoExit -ExecutionPolicy Bypass -File `"$scriptPath`""
$shortcut.WorkingDirectory = $PSScriptRoot
$shortcut.WindowStyle = 1
$shortcut.IconLocation = "powershell.exe,0"
$shortcut.Description = "Lance le serveur de preview local du site Robin Duale"
$shortcut.Save()

Write-Host "Raccourci cree : $shortcutPath"
Write-Host ""
Write-Host "Pour epingler a la barre des taches :"
Write-Host "  Clic droit sur le raccourci du Bureau -> Epingler a la barre des taches"
