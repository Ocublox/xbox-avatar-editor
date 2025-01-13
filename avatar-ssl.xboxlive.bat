@echo off
title Xbox Avatar Editor
set CURRENT_DIR=%~dp0

if not exist "%CURRENT_DIR%gmesh.exe" (
    echo gmesh.exe not found!
    choice /c yn /m "Would you like to download gmesh.exe?"
    if errorlevel 2 (
        exit
    ) else (
        curl -L "https://github.com/PMZeroSkyline/GPA-Mesh/releases/download/Release/gmesh.exe" -o "%CURRENT_DIR%gmesh.exe"
    )
)

:main
cls

set /p name=Enter model name (without extension): 
%CURRENT_DIR%gmesh -s TEXCOORD %name%.csv %name%.obj %name%_build.obj
pause
goto main