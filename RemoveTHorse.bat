del /q C:\Users\"%USERNAME%"\AppData\Roaming\explorer.exe
reg delete HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run /v winexplorer  /f
cls
echo "[*] DONE "
echo "[*] Please Restart Your System!"
pause