import os
import time
from datetime import datetime, timedelta
import platform
import subprocess
import shutil

TEMP_FOLDERS = [
    os.path.expanduser("~\\AppData\\Local\\Temp"),
    "/tmp",
]
TEMP_EXTENSIONS = ['.tmp', '.log', '.cache', '.bak']
MAX_SIZE_MB = 100
DAYS_OLD = 30

base_dir = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(base_dir, "reporte")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "limpieza_log.txt")

def bytes_to_mb(size):
    return size / (1024 * 1024)

def write_log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

def find_files_to_delete(paths, exts, max_size_mb, days_old):
    now = datetime.now()
    files_to_delete = []
    for path in paths:
        if not os.path.exists(path):
            write_log(f"Ruta no encontrada: {path}")
            continue
        for root, dirs, files in os.walk(path):
            for file in files:
                try:
                    filepath = os.path.join(root, file)
                    stat = os.stat(filepath)
                    size_mb = bytes_to_mb(stat.st_size)
                    mod_time = datetime.fromtimestamp(stat.st_mtime)
                    ext = os.path.splitext(file)[1].lower()
                    if (ext in exts or size_mb >= max_size_mb or (now - mod_time).days >= days_old):
                        files_to_delete.append((filepath, size_mb, mod_time))
                except Exception as e:
                    write_log(f"Error leyendo archivo {filepath}: {e}")
    return files_to_delete

def eliminar_carpetas_vacias(paths):
    for path in paths:
        if not os.path.exists(path):
            continue
        for root, dirs, files in os.walk(path, topdown=False):
            for d in dirs:
                dirpath = os.path.join(root, d)
                try:
                    if not os.listdir(dirpath):
                        os.rmdir(dirpath)
                        print(f"Carpeta vacía eliminada: {dirpath}")
                        write_log(f"Carpeta vacía eliminada: {dirpath}")
                except Exception as e:
                    print(f"Error eliminando carpeta {dirpath}: {e}")
                    write_log(f"Error eliminando carpeta {dirpath}: {e}")

def confirm_and_delete(files):
    print(f"Se encontraron {len(files)} archivos candidatos para borrar:")
    for i, (f, size, mtime) in enumerate(files, 1):
        print(f"{i}. {f} | {size:.2f} MB | modificado: {mtime.strftime('%Y-%m-%d')}")
    confirm = input("¿Deseas borrar todos estos archivos? (s/n): ").lower()
    if confirm == 's':
        write_log(f"Inicio de limpieza: {len(files)} archivos a borrar.")
        for f, size, mtime in files:
            try:
                os.remove(f)
                print(f"Borrado: {f}")
                write_log(f"Archivo borrado: {f} | Tamaño: {size:.2f} MB | Modificado: {mtime.strftime('%Y-%m-%d')}")
            except Exception as e:
                print(f"Error borrando {f}: {e}")
                write_log(f"Error borrando {f}: {e}")
        eliminar_carpetas_vacias(TEMP_FOLDERS)
        write_log("Limpieza finalizada.\n")
    else:
        print("No se borró ningún archivo.")
        write_log("Limpieza cancelada por el usuario.\n")

def main():
    write_log("=== Nueva ejecución de limpieza automática ===")
    print("Buscando archivos temporales y grandes para limpiar...")
    files = find_files_to_delete(TEMP_FOLDERS, TEMP_EXTENSIONS, MAX_SIZE_MB, DAYS_OLD)
    confirm_and_delete(files)

if __name__ == "__main__":
    main()
