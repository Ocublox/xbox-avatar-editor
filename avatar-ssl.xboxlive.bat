@echo off
title Xbox Avatar Editor
set CURRENT_DIR=%~dp0

if not exist "%CURRENT_DIR%gmesh.exe" (
    echo gmesh.exe / meshedit.exe not found!
    choice /c yn /m "Would you like to download missing files?"
    if errorlevel 2 (
        exit
    ) else (
        cls
        curl -L "https://github.com/PMZeroSkyline/GPA-Mesh/releases/download/Release/gmesh.exe" -o "%CURRENT_DIR%gmesh.exe"
        cls
        curl -L "https://github.com/Ocublox/xbox-avatar-editor/releases/download/Main/meshedit.exe" -o "%CURRENT_DIR%meshedit.exe"
    )
)

:main
cls
echo Make sure the exported OBJ has the same name as the CSV.
set /p name=Enter model name: 
%CURRENT_DIR%gmesh -s TEXCOORD %name%.csv %name%.obj %name%_temp.obj
%CURRENT_DIR%meshedit %name%_temp.obj %name%_build.obj
del %name%_temp.obj
pause
goto main