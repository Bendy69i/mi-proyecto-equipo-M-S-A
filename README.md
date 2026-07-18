# Secure-TCP-Chat

Secure-TCP-Chat es un chat cifrado en Python mediante sockets TCP y SSL/TLS, contando con una interfaz grafica (GUI) construida mediante Tkinter. El Proyecto fue desarrollado durante el curso intensivo de Python Ofensivo de la academia Hack4u, impartido por S4vitar.

---

## Overview

Secure-TCP-Chat es un programa de chat en tiempo real con interfaz gráfica que se comunica mediante sockets TCP cifrados con SSL/TLS. Utiliza las librerías `Tkinter`, `Tkinter.scrolledtext`, `socket`, `ssl` y `threading`.

Como medida de seguridad e implementacion a conocimientos de Hacking, toda la comunicación entre cliente y servidor viaja cifrada, evitando que un atacante en la misma red pueda leer los mensajes mediante técnicas de Man In The Middle (MITM) o captura de tráfico (por ejemplo, con `tshark` o `WireShark`).

---

## Características y funciones

- Toda la comunicación esta cifrada con TLS/SSL 
- Interfaz gráfica implementada con Tkinter
- Soporte para múltiples clientes simultáneos mediante `threading`, separando hilos
- Listado de usuarios conectados mediante el comando `!usuarios` con un botón
- Se notifica cuando un usuario entra y sale del chat
- Si se presenta una falla, se cierran los hilos con la implementacion Daemon True

---

## Tree

```
.
├── client.py 
├── server.py
├── server-key.key
├── server.csr
└── server-cert.pem
```

---

## Requisitos

- Python 3.x
- Módulos estándar: `tkinter`, `ssl`, `socket`, `threading` (incluidos en la instalación base de Python)
- OpenSSL, para la generación del certificado

### Nota 
La funcion `ssl.wrap_socket()` quedo obsoleta, se tiene que usar la que esta en el programa si se toma en cuenta que se quieren hacer modificaciones

---

## Generación del certificado SSL

El servidor requiere un certificado y una clave privada para cifrar la conexión. Estos se generan con OpenSSL, para eso se ejecutan:

```bash
# 1. Generar la clave privada RSA cifrada con AES-256
openssl genpkey -algorithm RSA -out server-key.key -aes256

# 2. Generar la solicitud de firma del certificado (CSR)
openssl req -new -key server-key.key -out server.csr

# 3. Firmar el certificado con la propia clave (autofirmado), válido 365 días
openssl x509 -req -days 365 -in server.csr -signkey server-key.key -out server-cert.pem

# 4. Eliminar la contraseña de la clave privada, necesario para que el servidor la cargue sin solicitar passphrase
openssl rsa -in server-key.key -out server-key.key
```

Al finalizar se obtienen los tres archivos, tienen que tener el mismo nombre que el comando debido a que asi se agrego en el programa, caba destacar que de igual manera deben de estar en el mismo directorio: `server-key.key`, `server.csr` y `server-cert.pem`

### Verificación del cifrado del tráfico

Una comprobacion para el funcionamiento del encriptado, se usa `tshark`:

```bash
tshark -i lo -Tfields -e data.data
```

Si el chat no estuviera cifrado, sería posible reconstruir el mensaje original a partir del hexadecimal capturado con el comando

```bash
echo -n "<cadena_en_hex>" | tr -d ':' | xxd -ps -r; echo
```

Con SSL/TLS activo, la cadena capturada corresponde al contenido cifrado y este comando no devuelve texto legible, lo cual confirma que la comunicación está protegida.

---

## Uso

### Iniciar el servidor

```bash
python3 server.py
```

o 

```bash
chmod +x server.py client.py
./server.py
```

El servidor queda a la escucha de conexiones en `localhost:1234`, este servidor a su vez puede montarse como servicio en una VPS cambiando las ip's correspondientes

### Iniciar el cliente

```bash
python3 client.py
```
o 

```bash
./client.py
```


Se solicita un nombre de usuario por consola y a continuación se abre la ventana del chat.

### Comandos disponibles

| Comando | Descripción |
|---|---|
| `!usuarios` | Muestra la lista de usuarios conectados actualmente (Futura implementacion )|

El botón "Listar usuarios" de la interfaz invoca este mismo comando sin necesidad de escribirlo.

---

## Detalles técnicos a destacar

- Los hilos de recepción de mensajes (`receive_message`) se ejecutan como daemon threads (`thread.daemon = True`). Esto garantiza que, al cerrar la ventana principal de Tkinter, los hilos en segundo plano no impidan la finalización correcta del programa
- El cifrado se implementa mediante `ssl._create_unverified_context()` en el cliente y `ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)` en el servidor, cargando el par certificado/clave generado con OpenSSL.

---

## Future Improvements

El proyecto es funcional pero fue construido con fines educativos, por lo que existen mejoras identificadas y pendientes de implementar:

- Bloqueo ocasional de la GUI: Tkinter está diseñado para ejecutarse en un único hilo principal. Dado que la recepción de mensajes corre en un hilo secundario que actualiza directamente los widgets, en determinados escenarios la interfaz puede volverse poco responsiva o bloquearse. Una solución más robusta consistiría en usar una cola (`queue.Queue`) para comunicar el hilo de red con el hilo principal de Tkinter
- Migración de la GUI a CustomTkinter, con el objetivo de lograr una interfaz más moderna y con mejor soporte de temas
- Ampliación del sistema de comandos, siguiendo un esquema similar al de plataformas de chat en vivo (por ejemplo Twitch). Actualmente solo existe `!usuarios`; se contempla añadir:   
  - `!usuarios`, implementacion del comando para listar sin presionar el botón
  - `!ayuda`, para mostrar los comandos disponibles
  - `!privado <usuario> <mensaje>`, para el envío de mensajes privados
  - `!kick <usuario>`, para moderación desde el servidor
- Validación de certificados: el cliente utiliza actualmente un contexto SSL sin verificación (`_create_unverified_context`), adecuado para pruebas locales. En un entorno de producción sería necesario validar correctamente el certificado del servidor
- Manejo de errores más granular: los bloques `except` genéricos podrían especificarse para distinguir desconexiones normales de errores reales

---

## Créditos

Proyecto desarrollado en el marco del curso Ofensive Python de la academia [Hack4u](https://hack4u.io), impartido por S4vitar.



--Nitblan :))
