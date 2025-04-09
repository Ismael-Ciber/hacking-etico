#!/bin/bash

URL="$1"

if [ -z "$URL" ]; then
    echo "Para usar el script debes usar este formato: ./http_checker.sh mercadona.com"
    exit 1
fi

if curl --silent --head --fail "$URL" > /dev/null; then
    echo "La página $URL está en línea."
else
    echo "La página $URL no está disponible."
fi
