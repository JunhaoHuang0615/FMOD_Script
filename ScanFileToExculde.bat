@echo off

:: Check if a parameter is provided
if "%~1"=="" (
    echo Usage: %0 PathToScan
    goto :eof
)

:: Set the path to scan from the command line argument
set "PathToScan=%~1"

:: Check if the specified directory exists
if not exist "%PathToScan%" (
    echo Directory does not exist: "%PathToScan%"
    goto :eof
)

:: Use a "for" loop to iterate over all files in the specified directory and its subdirectories
for /r "%PathToScan%" %%F in (*) do (
    echo %%~nxF
)

:end