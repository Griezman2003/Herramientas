import os
import json
import time
import getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from base64 import urlsafe_b64encode
from colorama import init, Fore, Style
import tkinter as tk
from tkinter import simpledialog, messagebox

init(autoreset=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "passwords.enc")
EXPORT_PATH = os.path.join(BASE_DIR, "passwords_export.json")
SALT_PATH = os.path.join(BASE_DIR, "salt.bin")
MASTER_KEY_PATH = os.path.join(BASE_DIR, "master.key")

os.makedirs(BASE_DIR, exist_ok=True)

INACTIVITY_TIMEOUT = 120

def generate_salt():
    return os.urandom(16)

def load_salt():
    if not os.path.exists(SALT_PATH):
        salt = generate_salt()
        with open(SALT_PATH, "wb") as f:
            f.write(salt)
        return salt
    else:
        with open(SALT_PATH, "rb") as f:
            return f.read()

SALT = load_salt()

def derive_key(password: str) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=390000,
    )
    key = urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def encrypt_data(data: dict, fernet: Fernet) -> bytes:
    json_data = json.dumps(data).encode()
    return fernet.encrypt(json_data)

def decrypt_data(token: bytes, fernet: Fernet) -> dict:
    try:
        decrypted = fernet.decrypt(token)
        return json.loads(decrypted.decode())
    except Exception:
        return {}

def save_passwords(data: dict, fernet: Fernet):
    encrypted = encrypt_data(data, fernet)
    with open(FILE_PATH, "wb") as f:
        f.write(encrypted)

def load_passwords(fernet: Fernet) -> dict:
    if not os.path.exists(FILE_PATH):
        return {}
    with open(FILE_PATH, "rb") as f:
        encrypted = f.read()
    return decrypt_data(encrypted, fernet)
    
def normalize_data(data):
    """
    Convierte entradas antiguas tipo {"servicio": "contraseña"} a {"servicio": {"password": "...", "tags": []}}
    """
    for service, value in list(data.items()):
        if isinstance(value, str):
            data[service] = {"password": value, "tags": []}
    return data

def save_master_key(key: bytes):
    with open(MASTER_KEY_PATH, "wb") as f:
        f.write(key)

def load_master_key() -> bytes:
    if not os.path.exists(MASTER_KEY_PATH):
        return None
    with open(MASTER_KEY_PATH, "rb") as f:
        return f.read()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print(Fore.CYAN + Style.BRIGHT + "=== Gestor Avanzado de Contraseñas ===\n")

# Ahora cada entrada es:
# service_name: { "password": "...", "tags": ["tag1", "tag2"] }

def list_passwords(data):
    if not data:
        print(Fore.YELLOW + "No hay contraseñas guardadas.")
        return
    print(Fore.MAGENTA + "\n🔐 Contraseñas guardadas:\n")
    for service, info in data.items():
        tags = ", ".join(info.get("tags", []))
        print(Fore.GREEN + f"- {service} [{tags}]: " + Fore.WHITE + info.get("password", ""))

def add_password(data):
    service = input(Fore.CYAN + "Nombre del servicio o sitio: ").strip()
    if not service:
        print(Fore.RED + "Servicio inválido.")
        return
    pwd = input(Fore.CYAN + "Contraseña: ").strip()
    tags_raw = input(Fore.CYAN + "Etiquetas o categorías (separadas por comas): ").strip()
    tags = [tag.strip() for tag in tags_raw.split(",")] if tags_raw else []
    data[service] = {"password": pwd, "tags": tags}
    print(Fore.GREEN + f"✔ Contraseña guardada para: {service}")

def search_password(data):
    query = input(Fore.CYAN + "Buscar servicio o etiqueta: ").strip().lower()
    found = False
    for service, info in data.items():
        if query in service.lower() or any(query in tag.lower() for tag in info.get("tags", [])):
            tags = ", ".join(info.get("tags", []))
            print(Fore.MAGENTA + f"{service} [{tags}]: " + Fore.WHITE + info.get("password", ""))
            found = True
    if not found:
        print(Fore.YELLOW + f"No se encontró ninguna contraseña para '{query}'")

def edit_password(data):
    service = input(Fore.CYAN + "Nombre del servicio a editar: ").strip()
    if service not in data:
        print(Fore.RED + f"No existe el servicio '{service}'.")
        return
    new_pwd = input(Fore.CYAN + "Nueva contraseña (deja vacío para no cambiar): ").strip()
    tags_raw = input(Fore.CYAN + "Nuevas etiquetas (separadas por comas, deja vacío para no cambiar): ").strip()
    if new_pwd:
        data[service]["password"] = new_pwd
    if tags_raw:
        tags = [tag.strip() for tag in tags_raw.split(",")]
        data[service]["tags"] = tags
    print(Fore.GREEN + f"Contraseña actualizada para: {service}")

def delete_password(data):
    service = input(Fore.CYAN + "Nombre del servicio a eliminar: ").strip()
    if service not in data:
        print(Fore.RED + f"No existe el servicio '{service}'.")
        return
    confirm = input(Fore.RED + f"¿Seguro que quieres eliminar '{service}'? (s/n): ").lower()
    if confirm == 's':
        del data[service]
        print(Fore.GREEN + f"Servicio '{service}' eliminado.")

def export_passwords(data):
    if not data:
        print(Fore.YELLOW + "No hay datos para exportar.")
        return
    with open(EXPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(Fore.GREEN + f"Contraseñas exportadas a: {EXPORT_PATH}")

def import_passwords(data):
    if not os.path.exists(EXPORT_PATH):
        print(Fore.RED + f"No se encontró archivo de exportación en {EXPORT_PATH}")
        return
    with open(EXPORT_PATH, "r", encoding="utf-8") as f:
        imported = json.load(f)
    data.update(imported)
    print(Fore.GREEN + f"Contraseñas importadas desde: {EXPORT_PATH}")

def create_master_password():
    while True:
        clear_screen()
        print(Fore.CYAN + Style.BRIGHT + "=== Crear Contraseña Maestra ===\n")
        pwd1 = getpass.getpass(Fore.CYAN + "Introduce nueva contraseña maestra: ")
        pwd2 = getpass.getpass(Fore.CYAN + "Confirma la contraseña maestra: ")
        if pwd1 != pwd2:
            print(Fore.RED + "Las contraseñas no coinciden. Intenta de nuevo.")
            time.sleep(2)
        elif len(pwd1) < 8:
            print(Fore.RED + "La contraseña debe tener al menos 8 caracteres.")
            time.sleep(2)
        else:
            key = derive_key(pwd1)
            save_master_key(key)
            print(Fore.GREEN + "Contraseña maestra creada con éxito.")
            time.sleep(2)
            return key

def print_access_banner():
    ascii_banner_access = r"""
   ____                _                   _                 
  / ___|___  _ __  ___| |_ _ __ _   _  ___| |_ ___  _ __ ___ 
 | |   / _ \| '_ \/ __| __| '__| | | |/ __| __/ _ \| '__/ __|
 | |__| (_) | | | \__ \ |_| |  | |_| | (__| || (_) | |  \__ \
  \____\___/|_| |_|___/\__|_|   \__,_|\___|\__\___/|_|  |___/

        GESTOR DE CONTRASEÑAS - ACCESO
    """
    print(Fore.MAGENTA + ascii_banner_access)

def verify_master_password():
    saved_key = load_master_key()
    if not saved_key:
        return None

    for attempt in range(3):
        pwd = getpass.getpass(Fore.CYAN + "Introduce tu contraseña maestra: ")
        key = derive_key(pwd)
        if key == saved_key:
            return key
        print(Fore.RED + "Contraseña incorrecta.")
    return None


def launch_gui(data, fernet):

    def gui_add_password():
        service = simpledialog.askstring("Agregar contraseña", "Nombre del servicio o sitio:")
        if not service:
            return
        pwd = simpledialog.askstring("Agregar contraseña", f"Contraseña para {service}:", show="*")
        if pwd is None:
            return
        tags_raw = simpledialog.askstring("Agregar contraseña", "Etiquetas o categorías (separadas por comas):")
        tags = [tag.strip() for tag in tags_raw.split(",")] if tags_raw else []
        data[service] = {"password": pwd, "tags": tags}
        save_passwords(data, fernet)
        messagebox.showinfo("Éxito", f"Contraseña guardada para: {service}")

    def gui_list_passwords():
        output = ""
        if not data:
            output = "No hay contraseñas guardadas."
        else:
            for service, info in data.items():
                tags = ", ".join(info.get("tags", []))
                output += f"{service} [{tags}]: {info.get('password', '')}\n"
        messagebox.showinfo("Listado de contraseñas", output)

    def gui_search_password():
        query = simpledialog.askstring("Buscar contraseña", "Servicio o etiqueta:")
        if not query:
            return
        found = False
        output = ""
        for service, info in data.items():
            if query.lower() in service.lower() or any(query.lower() in tag.lower() for tag in info.get("tags", [])):
                tags = ", ".join(info.get("tags", []))
                output += f"{service} [{tags}]: {info.get('password', '')}\n"
                found = True
        if not found:
            output = f"No se encontró ninguna contraseña para '{query}'"
        messagebox.showinfo("Resultado búsqueda", output)

    root = tk.Tk()
    root.title("Gestor de Contraseñas - GUI")
    root.geometry("350x200")

    tk.Button(root, text="Agregar contraseña", command=gui_add_password).pack(fill="x", padx=10, pady=5)
    tk.Button(root, text="Listar contraseñas", command=gui_list_passwords).pack(fill="x", padx=10, pady=5)
    tk.Button(root, text="Buscar contraseña", command=gui_search_password).pack(fill="x", padx=10, pady=5)
    tk.Button(root, text="Salir", command=root.destroy).pack(fill="x", padx=10, pady=20)

    root.mainloop()

def main():
    clear_screen()

    print_access_banner()

    key = load_master_key()
    if not key:
        key = create_master_password()
    else:
        key = verify_master_password()
        if not key:
            print(Fore.RED + "Demasiados intentos fallidos. Saliendo...")
            return

    fernet = Fernet(key)
    data = normalize_data(load_passwords(fernet))
    last_activity = time.time()

    ascii_banner_menu = r"""
   ____                _                   _
  / ___|___  _ __  ___| |_ _ __ _   _  ___| |_ ___  _ __ ___
 | |   / _ \| '_ \/ __| __| '__| | | |/ __| __/ _ \| '__/ __|
 | |__| (_) | | | \__ \ |_| |  | |_| | (__| || (_) | |  \__ \
  \____\___/|_| |_|___/\__|_|   \__,_|\___|\__\___/|_|  |___/

        GESTOR DE CONTRASEÑAS - MENÚ PRINCIPAL
    """

    while True:
        if time.time() - last_activity > INACTIVITY_TIMEOUT:
            print(Fore.RED + "\n¡Inactividad detectada! Se requiere la contraseña maestra para continuar.\n")
            print_access_banner() 
            key = verify_master_password()
            if not key:
                print(Fore.RED + "Demasiados intentos fallidos. Cerrando sesión...")
                break
            fernet = Fernet(key)
            data = load_passwords(fernet)
            last_activity = time.time()

        clear_screen()
        print(Fore.MAGENTA + ascii_banner_menu) 

        print(Fore.GREEN + "Opciones:")
        print(Fore.YELLOW + "1. Agregar contraseña")
        print("2. Listar contraseñas")
        print("3. Buscar contraseña")
        print("4. Editar contraseña")
        print("5. Eliminar contraseña")
        print("6. Exportar contraseñas")
        print("7. Importar contraseñas")
        print("8. Cambiar contraseña maestra")
        print("9. Interfaz gráfica (GUI)")
        print("10. Salir")

        choice = input(Fore.GREEN + "\nElige una opción: ").strip()
        last_activity = time.time()

        if choice == "1":
            add_password(data)
        elif choice == "2":
            list_passwords(data)
        elif choice == "3":
            search_password(data)
        elif choice == "4":
            edit_password(data)
        elif choice == "5":
            delete_password(data)
        elif choice == "6":
            export_passwords(data)
        elif choice == "7":
            import_passwords(data)
        elif choice == "8":
            new_key = create_master_password()
            if new_key:
                fernet = Fernet(new_key)
                save_passwords(data, fernet)
                key = new_key
        elif choice == "9":
            launch_gui(data, fernet)
        elif choice == "10":
            print(Fore.RED + "Saliendo... Hasta luego!")
            save_passwords(data, fernet)
            break
        else:
            print(Fore.RED + "Opción no válida.")

        save_passwords(data, fernet)
        input(Fore.GREEN + "\nPresiona Enter para continuar...")

if __name__ == "__main__":
    main()
