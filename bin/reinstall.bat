@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

set BASE_DIR=C:\laragon\www
cd /d %BASE_DIR%

cls
echo.
echo ===================================================
echo  ███╗   ██╗██╗ ██████╗ ██████╗ ███████╗████████╗
echo  ████╗  ██║██║██╔═══██╗██╔══██╗██╔════╝╚══██╔══╝
echo  ██╔██╗ ██║██║██║   ██║██████╔╝█████╗     ██║   
echo  ██║╚██╗██║██║██║   ██║██╔═══╝ ██╔══╝     ██║   
echo  ██║ ╚████║██║╚██████╔╝██║     ███████╗   ██║   
echo  ╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═╝     ╚══════╝   ╚═╝   
echo.
echo       🌀 LARAVEL MIGRATE 🌀
echo ===================================================
echo.

for /d %%P in (*) do (
    if exist "%%P\artisan" (
        echo ===================================================
        echo Proyecto: %%P
        cd /d "%BASE_DIR%\%%P"
        call php artisan migrate:fresh
        call php artisan db:seed
        echo.
    )
)
echo.