@echo off
if "%2"=="" (
    exit /b 1
)
php artisan make:%1 %2
