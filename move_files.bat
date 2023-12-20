@echo off
setlocal enabledelayedexpansion

:: 在FMod使用的时候，需要把这个bat放在
:: Check if two parameters are provided
if "%~2"=="" (
    echo Usage: %0 SourcePath DestinationPath
    goto :eof
)

:: Set source and destination paths from command line arguments
set "SourcePath=%~1"
set "DestinationPath=%~2"

:: Check if the source directory exists
if not exist "%SourcePath%" (
    echo Source directory does not exist: "%SourcePath%"
    goto :eof
)

:: Check if the destination directory exists, create it if not
if not exist "%DestinationPath%" (
    mkdir "%DestinationPath%"
)

:: Ensure that all files in the destination folder are accessible and writable
for /r "%DestinationPath%" %%I in (*) do (
    attrib -r "%%I" 2>nul
)

:: Copy files and folders from the source to the destination
xcopy /s /i /y "%SourcePath%" "%DestinationPath%"

:: Delete files in the destination directory that don't exist in the source directory (based on filename)
:: D就是for循环的变量， %%~nxD：  %%~n 表示提取文件名（不包括扩展名） %%~x 表示提取扩展名。 %%~nx 用于从文件路径中提取文件名和扩展名
for /r "%DestinationPath%" %%D in (*) do (
    set "DeleteFile=True"
    set "DestinationFileName=%%~nD"
    
    for /r "%SourcePath%" %%S in (*) do (
        set "SourceFileName=%%~nS"
        if "%%~nD" == "%%~nS" (
            set "DeleteFile=False"
        ) else if "%%~nD.bank" == "%%~nS"(
            set "DeleteFile=False"
        )
    )

    if "!DeleteFile!" == "True" (
        del "%%D"
    )
)

echo All files and folders copied from "%SourcePath%" to "%DestinationPath%"

:end