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

REM Read the first line (header) of the CSV
set "header="
for /f "usebackq delims=" %%a in ("%name%.csv") do (
    set "header=%%a"
    goto :process
)

:process
echo.

REM Extract all TEXCOORD columns dynamically
for /f "tokens=* delims=," %%a in ("%header%") do (
    set "line=%%a"
)

REM Replace commas with spaces and check each column
for %%i in (%header%) do (
    echo %%i | findstr /B "TEXCOORD" >nul
    if not errorlevel 1 (
        echo Processing %%i...
        "%CURRENT_DIR%gmesh" -s %%i %name%.csv %name%.obj %name%_temp.obj
        "%CURRENT_DIR%meshedit" %name%_temp.obj %name%_%%i.obj
        del %name%_temp.obj
	echo.
    )
)

echo All TEXCOORD columns processed!
pause
goto main
