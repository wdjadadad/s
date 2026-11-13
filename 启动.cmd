@echo off
setlocal
cd /d "%~dp0"
title ETS Answer Getter v2.0.0

set "PYEXE="
for /f "delims=" %%I in ('where py 2^>nul') do if not defined PYEXE set "PYEXE=%%~fI"
if not defined PYEXE if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" set "PYEXE=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
if not defined PYEXE if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" set "PYEXE=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"

if not defined PYEXE (
    echo [!] Python 3.10+ not found. Install it and tick "Add python.exe to PATH".
    pause
    exit /b 1
)

rem New ETS client keeps its cache in %APPDATA%\ETS; the hex-named folder is
rem the older client.  Prefer the new one, fall back to the old one.
set "ROOT=%APPDATA%\ETS"
if not exist "%ROOT%" set "ROOT=%APPDATA%\74656D705F74656D705F74656D705F74002"
if not exist "%ROOT%" set "ROOT=%APPDATA%"

echo Python  : %PYEXE%
echo Scan dir: %ROOT%
echo A browser window will open. Close THIS window to stop the program.
echo.
"%PYEXE%" "%~dp0run.py" --web --root "%ROOT%"
echo.
echo Program exited.
pause
