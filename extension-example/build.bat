@echo off
setlocal enabledelayedexpansion

:: Step 1: Get the target version from input
set /p version="Enter the target version: "

:: Step 2: Create the build folder
if exist build rd /s /q build
mkdir build
mkdir build\res

:: Step 3: Copy all files from ./res to the build\res folder
xcopy /E /I /Y res\* build\res

:: Step 4: Compile all .py scripts from the build\res folder to .pyc using Python2
python -m compileall build\res

:: Step 5: Remove all .py scripts from the build\res folder
del /s /q build\res\*.py

:: Step 6: Read the contents of meta.xml and replace the pattern {{version}} with the input version
set "meta="
for /f "delims=" %%x in (meta.xml) do (
    set "line=%%x"
    set "line=!line:{{version}}=%version%!"
    set "meta=!meta!!line!"
)

:: Step 7: Create a new meta.xml file in the build folder with the replaced version
echo !meta! > build\meta.xml

:: Step 8: Create a zip archive with zero compression using 7-Zip
set target=example.data-provider-extension_%version%.wotmod
if exist %target% del /f /q %target%

:: Step 9: Ensure 7-Zip is in your PATH or specify the full path to 7z.exe
"C:\Program Files\7-Zip\7z.exe" a -tzip -mx=0 "%target%" .\build\*

:: Step 10: Clean up the build folder
rd /s /q build

echo Build complete: %target%
pause