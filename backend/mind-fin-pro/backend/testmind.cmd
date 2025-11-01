@echo off
setlocal
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0testmind.ps1"
exit /b %ERRORLEVEL%
