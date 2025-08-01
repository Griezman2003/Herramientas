@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

set DESTINO=C:\Users\chapa\Music

if not exist "%DESTINO%" mkdir "%DESTINO%"

color 0A

:MENU
cls
echo.
echo ===================================================
echo  ███╗   ██╗███████╗██╗   ██╗██╗   ██╗
echo  ████╗  ██║██╔════╝██║   ██║██║   ██║
echo  ██╔██╗ ██║█████╗  ██║   ██║██║   ██║
echo  ██║╚██╗██║██╔══╝  ╚██╗ ██╔╝██║   ██║
echo  ██║ ╚████║███████╗ ╚████╔╝ ╚██████╔╝
echo  ╚═╝  ╚═══╝╚══════╝  ╚═══╝   ╚═════╝ 
echo.
echo       🌀 DESCARGADOR MULTIMEDIA 🌀
echo ===================================================
echo.
echo [1] ▶ Descargar video + audio (MP4)
echo [2] 🎵 Descargar solo audio (MP3)
echo [3] 📁 Ver biblioteca y reproducir música
echo [4] ❌ Salir
echo ---------------------------------------------------
set /p opcion=🡆 Elige una opción (1-4): 

if "%opcion%"=="1" goto VIDEO
if "%opcion%"=="2" goto AUDIO
if "%opcion%"=="3" goto BIBLIOTECA
if "%opcion%"=="4" goto FIN

echo ❗ Opción inválida. Intenta de nuevo.
pause
goto MENU

:VIDEO
cls
echo.
echo ╔════════════════════════════════════════════╗
echo ║        DESCARGA DE VIDEO + AUDIO (MP4)     ║
echo ╚════════════════════════════════════════════╝
echo.
set /p URL=🔗 Introduce la URL del video o playlist: 
echo.
echo ▶ Descargando video + audio desde:
echo %URL%
echo.

yt-dlp.exe --newline -f bestvideo+bestaudio --merge-output-format mp4 -o "%DESTINO%\%%(title)s.%%(ext)s" "%URL%"

timeout /t 1 /nobreak >nul
goto MENU

:AUDIO
cls
echo.
echo ╔════════════════════════════════════════════╗
echo ║          DESCARGA SOLO AUDIO (MP3)         ║
echo ╚════════════════════════════════════════════╝
echo.
set /p URL=🔗 Introduce la URL del video o playlist: 
echo.
echo 🎵 Descargando solo audio desde:
echo %URL%
echo.

yt-dlp.exe --newline -x --audio-format mp3 -o "%DESTINO%\%%(title)s.%%(ext)s" "%URL%"

timeout /t 1 /nobreak >nul
goto MENU

:BIBLIOTECA
cls
echo Lanzando reproductor interactivo...
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0select-mp3.ps1"
goto MENU

:FIN
cls
echo.
echo Cerrando el programa...
timeout /t 2 /nobreak >nul
exit


