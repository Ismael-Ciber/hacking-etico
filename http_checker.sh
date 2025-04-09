#!/bin/bash

LISTA="$1"

if [ -z "$LISTA" ]; then
    echo "Para usar el script debes usar este formato: ./http_checker.sh mercadona.com"
    exit 1
fi

if [ ! -f "$LISTA" ]; then
    echo "El archivo $LISTA no existe."
    exit 1
fi

while read -r URL; do
    if curl --silent --head --fail "$URL" > /dev/null; then
        echo "La página $URL está en línea."
    else
        echo "La página $URL no está disponible."
    fi
done < "$LISTA"
