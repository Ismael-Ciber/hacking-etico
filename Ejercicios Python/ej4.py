import subprocess
import sys

if len(sys.argv) != 4:
    print("Uso: python3 brute_ping.py <IP_del_servidor> <numero_de_peticiones> <intervalo_en_segundos>")
    sys.exit(1)

ip_servidor = sys.argv[1]
num_peticiones = int(sys.argv[2])
intervalo = float(sys.argv[3])

# Construir el comando ping
comando = ["ping", "-i", str(intervalo), "-c", str(num_peticiones), ip_servidor]

# Ejecutar el comando
subprocess.run(comando)
