Invoke-Expression (&starship init powershell)

Set-PSReadlineOption -EditMode emacs

Import-Module PSReadLine
Set-PSReadLineOption -PredictionSource History
Set-PSReadlineKeyHandler -Key Tab -Function MenuComplete
Set-PSReadLineKeyHandler -Key UpArrow -Function HistorySearchBackward
Set-PSReadLineKeyHandler -Key DownArrow -Function HistorySearchForward

# $cde = @{
#   AUTO_CD = $false
#   CD_PATH = '~/Documents/', '~/Downloads'
# }
# Import-Module cd-extras
