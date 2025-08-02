import time
import os
from win10toast import ToastNotifier

apps_a_cerrar = [
    "chrome.exe",
    "code.exe",
    "WindowsTerminal.exe",
    "cmd.exe",
    "powershell.exe"
]

def cerrar_apps():
    for app in apps_a_cerrar:
        try:
            os.system(f"taskkill /f /im {app}")
        except:
            pass

def mostrar_notificacion():
    toaster = ToastNotifier()
    toaster.show_toast(
        "Recordatorio de sueño 😴",
        "Tu PC se apagará en 1 minuto.",
        duration=10
    )

def recordar_dormir():
    while True:
        hora_actual = time.strftime("%H:%M")
        if hora_actual == "22:05":
            mostrar_notificacion()

            print("¡Es hora de dormir 😴! Tu PC se apagará en 1 minuto.")
            time.sleep(60)
            cerrar_apps()
            os.system("shutdown /s /t 10 /f")
            break
        time.sleep(30)
recordar_dormir()
