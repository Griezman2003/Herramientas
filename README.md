# 🛠️ Herramientas Personales en Python

Colección de herramientas personales creadas con Python, diseñadas para automatizar tareas comunes desde la terminal de Windows. 

> ⚡ Incluye scripts en Python y accesos directos `.bat` para facilitar su uso desde cualquier ubicación.

---

## 📁 Estructura del proyecto

Herramientas/
│
├── # bin .bat para ejecutar desde cualquier terminal
│ ├── tool1.bat
│ ├── tool2.bat
│
├── # Scripts Python 
│ ├── tool1.py
│ ├── tool2.py
│
├── requirements.txt # Dependencias necesarias
├── setup.bat # Script de instalación automática
├── README.md # Este archivo

## 🚀 Instalación rápida

1. **Clona el repositorio**
   ```bash
   https://github.com/Griezman2003/Herramientas.git
   cd Herramientas


## 🚀 Finalización

2. **Corre el comando**
   ```bash
   setup.bat


## ✅ Comandos disponibles desde cualquier parte de tu terminal

| Comando   | Descripción                                |
|-----------|--------------------------------------------|
| `clima`   | Muestra el clima actual en tu ciudad       |
| `musica`  | Abre el reproductor de música y descarga              |
| `limpiar` | Limpia archivos temporales o basura del sistema |
| `p`  | Abre un guardado de contraseñas               |


## ✅ Comandos disponibles si trabajas desde laravel

| Comando   | Descripción                                |
|-----------|--------------------------------------------|
| `a`   | Crea modelos o controladores usando la sintaxis de laravel     |
| `cache`  | Realiza una limpieza de vistas y cache del proyecto              |


## ✅ Comandos disponibles si trabajas con GIT

| Comando   | Descripción                                |
|-----------|--------------------------------------------|
| `status`   | Realiza un status de tus cambios en tu proyecto       |
| `pull`  | Baja los cambios pendientes en tu repositorio              |
| `push`  | Sube los cambios pendientes en tu repositorio              |


# Recordatorio para Dormir 💤

Se agrega funcionalidad apaga tu PC automáticamente a una hora específica como recordatorio para dormir. Muestra una notificación antes de cerrar aplicaciones y apagar el sistema.

---

## 🛠 Requisitos

- Python 3 (solo si deseas modificar el script original)
- [`winotify`](https://pypi.org/project/winotify/) (para mostrar notificaciones en Windows)
- PyInstaller (si quieres compilar el `.exe`) (pyinstaller --onefile --noconsole dormir.py)
- crear tarea para ejecutar el .exe cada que se inicie el sistema 

---

