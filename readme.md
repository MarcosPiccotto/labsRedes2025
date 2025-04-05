# Home-made File Transfer Protocol (HFTP)

El protocolo 
HFTP es un protocolo ASCII, no binario, por lo que todo lo enviado (incluso archivos binarios) será legible por humanos como strings.

## Estructura

- Comandos: consisten en una cadena de caracteres compuesta por elementos separados por un Único espacio y terminadas con un fin de línea estilo DOS (\r\n)
1. El primer elemento del comando define el tipo de acción esperada por el comando y los elementos que siguen son argumentos necesarios para realizar la acción.

- Respuestas: comienza con una secuencia de dí­gitos (código de respuesta), seguida de un espacio, seguido de un texto describiendo el resultado de la operación. Por ejemplo, una cadena indicando un resultado exitoso tiene código 0 y con su texto descriptivo podrí­a ser 0 OK.

## Base64 
Base64 es un sistema de numeración posicional que usa 64 como base. Es la mayor potencia que puede ser representada usando Únicamente los caracteres imprimibles de ASCII.

Todas las variantes famosas que se conocen con el nombre de Base64 usan el rango de caracteres A-Z, a-z y 0-9 

## Comandos para poder correr el proyecto:

Para correr el proyecto podemos usar python3 normalmente pero si no queremos que se guarde la conexión en el puerto y tengamos que esperar a que expire el timeout debemos usar este comando:

_kill -9 $(lsof -ti :19500) ; python3 server.py -p 19500_

## Para usar el servidor con Telnet:
Esto es muy útil a la hora de realizar las pruebas ya que podemos llamar directamente a las funciones y ver su funcionamiento. 

_Telnet {ip} {puerto}_ sin ninguna flag.

# Implementación punto estrella: POLL

Poll es una llamada al sistema que te permite esperar por eventos en múltiples descriptores de archivo (como sockets). Esto es útil para manejar varios clientes a la vez sin tener que usar múltiples threads o procesos.

¿Cómo funciona?

-   Se registran todos los sockets (clientes conectados) en una estructura que maneja poll (como un poller en Python).

-   Se llama a poll() para que el sistema operativo revise cuál de ellos tiene algo para hacer (por ejemplo, datos para leer).

-   Se responde solo a esos sockets, sin bloquearte con los demás.