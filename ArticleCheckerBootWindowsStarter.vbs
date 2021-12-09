Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "cmd /c articleCheckerStarter.bat"
oShell.Run strArgs, 0, false