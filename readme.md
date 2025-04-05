# Home-made File Transfer Protocol (HFTP)

El protocolo 
HFTP es un protocolo ASCII, no binario, por lo que todo lo enviado (incluso archivos binarios) 
será legible por humanos como strings.

## Estructura

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

## Ventajas:
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

poll es una llamada al sistema que te permite esperar por eventos en múltiples descriptores de archivo (como sockets). Esto es útil para manejar varios clientes a la vez sin tener que usar múltiples threads o procesos.

Imaginá que tenés un servidor TCP que acepta conexiones de muchos clientes. Si usás accept() y luego recv() de forma secuencial para cada cliente, el servidor se va a quedar esperando por cada uno, uno por uno. Eso es ineficiente.

¿Cómo funciona?

-   Registrás todos los sockets (clientes conectados) en una estructura que maneja poll (como un poller en Python).

-   Llamás a poll() para que el sistema operativo te diga cuál de ellos tiene algo para hacer (por ejemplo, datos para leer).

-   Respondés solo a esos sockets, sin bloquearte con los demás.

¿Por qué los hilos son más costosos?
1. Overhead del sistema operativo

    Cada hilo necesita recursos: pila (stack), estructuras internas del SO, registros, etc.

    Si tenés cientos o miles de clientes, vas a tener cientos o miles de hilos, y eso consume mucha memoria y tiempo de CPU para cambiar entre hilos (context switching).

2. Cambio de contexto (context switch)

    Cuando el sistema operativo cambia de un hilo a otro, guarda y restaura registros, pila, etc.

    Si hay muchos hilos, pasa más tiempo cambiando entre hilos que haciendo trabajo útil.

Si estás haciendo un servidor tipo FTP o HTTP donde cada cliente hace peticiones puntuales, poll es ideal. Si estuvieras haciendo algo como un simulador físico donde cada cliente tiene una simulación intensiva, ahí podrían convenir los hilos.

implementacion pequeña explicacion:

esperar eventos en múltiples descriptores de archivo
self.poller = select.poll()
avisame cuando haya datos por leer "pollin"
self.poller.register(self.s, select.POLLIN)

Cuando hacés poller.register(socket, POLLIN), internamente poll() está monitoreando el descriptor de archivo

por lo tanto la forma de plantear va a ser(en simples palabras)
1) che tengo registrado este fd
    si -> verifico que tarea esta haciendo salida o entrada(pollin,pollout)
    no -> creo una nueva conexion y lo agrego a mi arreglo o lo que sea de bolsa de fd para luego ver si ya lo estoy usando
2) atender la tarea y dejarlo "dormir de nuevo", ya que solo laburamos con lo socket o fd que realmente piden hacer algo
3) cuando vamos cerrando sockets o clientes vamos liberando esos fd para que el SO sepa que puede asignar otra vez para otro socket. Como cada fd es unico tengo una forma de identificar a cada conexion en cada momento

poller.poll() te devuelve una lista tupla de eventos
ej: [(fd1, evento1), (fd2, evento2), ...]
cada evento es una mascara de bits la cual indica que hace

el & es el and pero de bit a bit, ya que comparamos los bits de event con los bits de cierto evento que nosotros queres identificar ej: event & select.POLLIN


Otros posibles flags:

    select.POLLINS listo para leer

    select.POLLOUT: listo para escribir

    select.POLLERR: ocurrió un error

    select.POLLHUP: el cliente cerró la conexión