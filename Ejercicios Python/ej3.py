import sys

ancho = int(sys.argv[1])
alto = int(sys.argv[2])
tipo = sys.argv[3]

if tipo == "simple":
    esquina_sup_izq = "┌"
    esquina_sup_der = "┐"
    esquina_inf_izq = "└"
    esquina_inf_der = "┘"
    linea_horiz = "─"
    linea_vert = "│"
elif tipo == "doble":
    esquina_sup_izq = "╔"
    esquina_sup_der = "╗"
    esquina_inf_izq = "╚"
    esquina_inf_der = "╝"
    linea_horiz = "═"
    linea_vert = "║"
else:
    esquina_sup_izq = tipo
    esquina_sup_der = tipo
    esquina_inf_izq = tipo
    esquina_inf_der = tipo
    linea_horiz = tipo
    linea_vert = tipo

# Imprimir la caja
print(esquina_sup_izq + linea_horiz * (ancho - 2) + esquina_sup_der)
for i in range(alto - 2):
    print(linea_vert + " " * (ancho - 2) + linea_vert)
print(esquina_inf_izq + linea_horiz * (ancho - 2) + esquina_inf_der)
