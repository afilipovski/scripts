Dim pythonScriptPath
pythonScriptPath = WScript.Arguments(0)

Dim shell
Set shell = CreateObject("WScript.Shell")

' Construct the command to run the Python script
Dim command
command = "python """ & pythonScriptPath & """"

' Run the command
Dim exitCode
shell.Run command, 0, True