' REFRESH_MACRO.vbs
' Double-click this file to refresh portfolio data and open the workbook.
' This is a Windows Script Host file (.vbs) that triggers the Python refresh.

Dim WshShell
Set WshShell = CreateObject("WScript.Shell")

Dim scriptDir
scriptDir = Left(WScript.ScriptFullName, InStrRev(WScript.ScriptFullName, "\"))

' Run the Python refresh
WshShell.CurrentDirectory = scriptDir & "scripts"
Dim result
result = WshShell.Run("python -B main.py", 1, True)

If result = 0 Then
    ' Open the workbook
    Dim xlPath
    xlPath = scriptDir & "output\Pokemon_Portfolio_Intelligence.xlsx"
    WshShell.Run """" & xlPath & """"
    MsgBox "Refresh complete! Workbook is opening.", vbInformation, "Portfolio Intelligence"
Else
    MsgBox "Refresh failed. Check output\portfolio_refresh.log for details.", vbExclamation, "Portfolio Intelligence"
End If

Set WshShell = Nothing
