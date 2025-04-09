# Home-made File Transfer Protocol (HFTP)

El protocolo HFTP es un protocolo ASCII, no binario, por lo que todo lo enviado (incluso archivos binarios) será legible por humanos como strings.

## Vídeo y presentación
- [Ver el vídeo en drive](https://drive.google.com/file/d/1-Ar7ARpzdoayingY55S8BIfBQeNDweEf/view?usp=sharing)
> Aclaración: El vídeo sin el punto estrella dura 10 minutos.
- [Presentación](https://docs.google.com/presentation/d/1IfkD3sdBDhzyF6rAfeXvQnrSmJSh4CoaOVlMhH-rRXU/edit?usp=sharing)


## Estructura

- Comandos: consisten en una cadena de caracteres compuesta por elementos separados por un único espacio y terminadas con un fin de línea estilo DOS (\r\n)1. El primer elemento del comando define el tipo de acción esperada por el comando y los elementos que siguen son argumentos necesarios para realizar la acción.

- Respuestas: comienza con una secuencia de dígitos (código de respuesta), seguida de un espacio, seguido de un texto describiendo el resultado de la operación. Por ejemplo, una cadena indicando un resultado exitoso tiene código 0 y con su texto descriptivo podría ser 0 OK.

## Base64 
Base64 es un sistema de numeración posicional que usa 64 como base. Es la mayor potencia que puede ser representada usando únicamente los caracteres imprimibles de ASCII.

Todas las variantes famosas que se conocen con el nombre de Base64 usan el rango de caracteres A-Z, a-z y 0-9.

# Comandos para poder correr el proyecto:

Para correr el proyecto podemos usar python3 normalmente pero si no queremos que se guarde la conexión en el puerto y tengamos que esperar a que expire el timeout debemos usar este comando:

_kill -9 $(lsof -ti :19500) ; python3 server.py -p 19500_

## Para usar el servidor con Telnet:
Esto es muy útil a la hora de realizar las pruebas ya que podemos llamar directamente a las funciones y ver su funcionamiento. 

_telnet {ip} {puerto}_ sin ninguna flag

> Aclaración: En caso de que la carpeta `testdata` no exista, se creará automáticamente.


## Como usar el cliente:
Ejecuta un cliente que usa todos los comandos realizados

_python3 client.py {ip} -p {puerto}_

# Preguntas que debiamos responder
## ¿Qué estrategias existen para poder implementar este mismo servidor pero con capacidad de atender múltiples clientes simultáneamente?

Una estrategia es el uso de Poll, una función que espera a que ocurra un evento entre uno o varios sockets. Es similar a select() pero con algunas ventajas (por ejemplo no tener limite máximo de sockets). Poll tiene la capacidad de "vigilar" los eventos que le interesen, como leer, escribir, etc, y bloquea el programa hasta que el evento ocurra y luego comunica en cuál socket sucedió y qué sucedió.

La otra forma es simplemente el uso de hilos, cuyo concepto basico sería: un anfitrion que recibe a los clientes en la entrada y cada hilo es un mesero que atiende a un cliente específico.

Su funcionamiento entonces es: El servidor espera nuevas conexiones, cuando llega la acepta y crea un hilo independiente para asignárselo. El hilo atiende la comunicación con el cliente y maneja la recepción y envío de datos. Cuando se desconecta, el hilo termina.

Ventajas: Cada cliente es atendido sin afectar a los demás, por ende, si un hilo tiene problemas no afecta al sistema en general. Esto mejora enormemente el uso de recursos en sistemas multicore.

Consideraciones: Demasiados hilos tienden a consumir mucha memoria y la sincronización para acceder a los recursos compartidos debe ser precisa.

## Pruebe ejecutar el servidor en una máquina del laboratorio, mientras utiliza el cliente desde otra, hacia la ip de la máquina servidor. ¿Qué diferencia hay si se corre el servidor desde la IP “localhost”, “127.0.0.1” o la ip “0.0.0.0”?

Para utilizar esta funcionalidad primero necesitamos saber la direccion IP de una compu, en este caso era 192.168.1.168. Entonces al iniciar el servidor debemos poner esa dirección en {address}, quedandonos el comando "python3 server.py -a 192.168.1.168" Utilizando otra computadora, debemos poner "python3 client.py 192.168.1.168 -p 19500". Hecho esto, probamos descargar desde el cliente los archivos que se encontraban en el servidor y funcionó perfectamente.

Ahora bien , la dirección 127.0.0.1 no nos sirve para establecer una conexión entre varias computadoras en la misma red local ya que es una dirección IP que se utiliza para referirse a la misma computadora, solo puede establecer una conexión con ella misma.

Por otra parte, la dirección 0.0.0.0 sí puede establecer una conexión en la red, pero únicamente si el cliente conoce la dirección IP de la computadora que hostea el servidor, así que a los efectos funciona igual que 192.168.1.168 en nuestro caso.