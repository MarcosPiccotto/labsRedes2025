# Home-made File Transfer Protocol (HFTP)

El protocolo 
HFTP es un protocolo ASCII, no binario, por lo que todo lo enviado (incluso archivos binarios) 
será legible por humanos como strings.

## estructura

- Comandos: consisten en una cadena de caracteres compuesta por elementos 
separados por un único espacio y terminadas con un fin de línea estilo DOS (\r\n)1. El 
primer elemento del comando define el tipo de acción esperada por el comando y los 
elementos que siguen son argumentos necesarios para realizar la acción.

- Respuestas: comienza con una secuencia de dígitos (código de respuesta), seguida de un espacio, seguido de un 
texto describiendo el resultado de la operación. Por ejemplo, una cadena indicando un 
resultado exitoso tiene código 0 y con su texto descriptivo podría ser 0 OK.

## Base64 
Base64 es un sistema de numeración posicional que usa 64 como base. Es la mayor potencia que puede ser representada usando únicamente los caracteres imprimibles de ASCII.

Todas las variantes famosas que se conocen con el nombre de Base64 usan el rango de caracteres A-Z, a-z y 0-9 

## ventajas:
- SMTP (Simple Mail Transfer Protocol), el protocolo usado para enviar correos electrónicos, fue diseñado para manejar solo texto ASCII de 7 bits.
- Muchos clientes de correo más antiguos no soportaban caracteres extendidos o datos binarios directamente. 
- Base64 evita estos problemas al representar todo en caracteres estándar (A-Z, a-z, 0-9, +, / y =).

## Desventajas de Base64

- Aumenta el tamaño del mensaje: Base64 aumenta el tamaño del archivo en un 33% aproximadamente, ya que por cada 3 bytes de datos, se generan 4 caracteres Base64.

- No es una forma de encriptación: Base64 solo codifica datos, pero no los protege contra ataques o accesos no autorizados.

# Socket
- Recomiendo leer: https://realpython.com/python-sockets/#python-socket-api-overview
## Métodos

- The primary socket API functions and methods in this module are:

    socket() -> crear el socket
    .bind() -> configurar la direccion y el puerto del servidor
    .listen() -> poner en modo escucha
    .accept() ->  espera a que un cliente se conecte
    .connect() -> efectivamente intenta conectarse
    .connect_ex()
    .send() -> mandar datos
    .recv() -> leer desde el buffer
    .close() -> cierra el socket

sudo fuser -k 19500/tcp

kill -9 $(lsof -ti :19500) ; python3 server.py -p 19500
