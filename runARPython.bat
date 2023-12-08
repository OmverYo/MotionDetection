@echo off
if not DEFINED IS_MINIMIZED set IS_MINIMIZED=1 && start "" /min "%~dpnx0" %* && exit
set scriptpath=%~dp0
"C:\Program Files\Python310\python.exe" "%scriptpath%\runARCompareApp.py"
exit(0)