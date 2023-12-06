@echo off
if not DEFINED IS_MINIMIZED set IS_MINIMIZED=1 && start "" /min "%~dpnx0" %* && exit
"C:\Program Files\Python310\python.exe" "C:\Users\pc1\Documents\GitHub\MetaPorts\Python\runARCompareApp.py"
exit(0)