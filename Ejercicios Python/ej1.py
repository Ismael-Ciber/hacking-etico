import sys

if len(sys.argv) != 2:
    print("Uso: python script.py <cadena_ARN>")
    sys.exit(1)

arn = sys.argv[1].upper()

if any(letra not in "AUGC" for letra in arn):
    print("Error: la cadena solo puede contener A, U, G y C.")
    sys.exit(1)

adn = arn.replace("U", "T")
print(adn)
