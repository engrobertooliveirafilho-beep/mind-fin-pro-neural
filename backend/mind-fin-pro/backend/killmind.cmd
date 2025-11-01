@echo off
setlocal
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0killmind.ps1"
exit /b %ERRORLEVEL%
