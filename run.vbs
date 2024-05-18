Set objShell = CreateObject("WScript.Shell")

strDirectory = "D:\Raspberry Pi Service Backups\.utils"

objShell.CurrentDirectory = strDirectory

objShell.Run "get_backup.bat", 0, True