@echo off
setlocal
echo.
echo == Instalando dependencias de Python ==

python -m pip install -r "%~dp0requirements.txt"

IF ERRORLEVEL 1 (
    echo Error al instalar dependencias. Verifica que tengas pip configurado correctamente.
    pause
    exit /b 1
)

echo.
echo == Agregando carpeta "bin" al PATH del usuario ==
set "SCRIPT_DIR=%~dp0bin"

REM
if "%SCRIPT_DIR:~-1%"=="\" set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

REM 
powershell -Command "$userPath = [Environment]::GetEnvironmentVariable('PATH', 'User'); if (-not $userPath.Contains('%SCRIPT_DIR%')) { [Environment]::SetEnvironmentVariable('PATH', $userPath + ';%SCRIPT_DIR%', 'User') }"

echo.
echo ✅ Instalación completada. Abre una nueva terminal para usar tus herramientas.
endlocal
pause
