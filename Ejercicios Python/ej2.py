import sys

texto = sys.argv[1]
cifrado = texto.translate(str.maketrans("OIEASGTBg", "013456789"))
print(cifrado)
