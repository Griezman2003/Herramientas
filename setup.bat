@echo off
echo Instalando dependencias de Python...
pip install -r requirements.txt

echo Agregando rutas al PATH de usuario...
setlocal

REM 
set SCRIPT_DIR=%~dp0bin

REM 
powershell -Command "[Environment]::SetEnvironmentVariable('PATH', $env:PATH + ';%SCRIPT_DIR%', 'User')"

echo Todo listo. Abre una nueva terminal para usar las herramientas.
endlocal
pause
