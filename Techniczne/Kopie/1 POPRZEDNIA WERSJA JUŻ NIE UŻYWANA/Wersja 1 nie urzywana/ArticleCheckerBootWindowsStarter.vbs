Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "cmd /c ArticleCheckerStarter.bat"
oShell.Run strArgs, 0, false