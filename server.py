#!/usr/bin/env python
# encoding: utf-8
# Revisión 2019 (a Python 3 y base64): Pablo Ventura
# Revisión 2014 Carlos Bederián
# Revisión 2011 Nicolás Wolovick
# Copyright 2008-2010 Natalia Bidart y Daniel Moisset
# $Id: server.py 656 2013-03-18 23:49:11Z bc $

from connection import Connection
from constants import *
import optparse
import os
import select
import socket
import sys

class Server:
    """
    El servidor, que crea y atiende el socket en la dirección y puerto
    especificados donde se reciben nuevas conexiones de clientes.
    """

    def __init__(self, addr=DEFAULT_ADDR, port=DEFAULT_PORT, directory=DEFAULT_DIR):
        self.dir = directory
        self.port = port
        self.addr = addr
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print("Serving %s on %s:%s." % (directory, addr, port))
        self.connections = {}
        
        if not os.path.exists(self.dir):
            os.makedirs(self.dir) 

    def serve(self):
        """
        Loop principal del servidor. Se acepta una conexión a la vez
        y se espera a que concluya antes de seguir.
        """
        self.s.bind((self.addr, self.port))
        self.s.listen()

        self.poller = select.poll()
        self.poller.register(self.s, select.POLLIN)

        try:
            while True:
                events = self.poller.poll()  # guardo todos eventos de los sockets
                for sock_fd, event in events:
                    if not (event & (select.POLLIN | select.POLLOUT)):
                        continue

                    if event & select.POLLOUT:  # el socket está listo para escribir
                        self.pollout_handle(sock_fd)
                    elif event & select.POLLIN:  # el socket está listo para leer
                        if sock_fd == self.s.fileno():  # el socket es el servidor
                            self.new_connection_handle()
                        else:  # el socket es un cliente
                            self.pollin_handle(sock_fd)
        except socket.error as e:
            print(f"Error en el socket: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")

    def new_connection_handle(self):
        try:
            new_client_socket, _ = self.s.accept()
            new_client_socket.setblocking(False)  # No bloquea cuando uso recv

            self.poller.register(
                new_client_socket, select.POLLIN
            )  # agrego el nuevo socket a la lista de sockets a monitorear
            self.connections[new_client_socket.fileno()] = Connection(
                new_client_socket, self.dir
            )
        except socket.error as e:
            print(f"Error al aceptar nueva conexión: {e}")

    def pollout_handle(self, sock_fd):
        client = self.connections[sock_fd]
        client.send()
        if not client.can_pollout():
            self.poller.modify(sock_fd, select.POLLIN)

    def pollin_handle(self, sock_fd):
        client = self.connections.get(sock_fd)

        if not client.handle():
            # Si el cliente cerró la conexión, lo eliminamos del monitoreo
            self.poller.unregister(sock_fd)
            del self.connections[sock_fd]
        elif client.can_pollout():  # Si el cliente tiene datos para enviar
            self.poller.modify(sock_fd, select.POLLIN | select.POLLOUT)
        else:  # Si no tiene datos para enviar
            self.poller.modify(sock_fd, select.POLLIN)


def main():
    """Parsea los argumentos y lanza el server"""

    parser = optparse.OptionParser()
    parser.add_option(
        "-p", "--port", help="Número de puerto TCP donde escuchar", default=DEFAULT_PORT
    )
    parser.add_option(
        "-a", "--address", help="Dirección donde escuchar", default=DEFAULT_ADDR
    )
    parser.add_option(
        "-d", "--datadir", help="Directorio compartido", default=DEFAULT_DIR
    )

    options, args = parser.parse_args()
    if len(args) > 0:
        parser.print_help()
        sys.exit(1)
    try:
        port = int(options.port)
    except ValueError:
        sys.stderr.write("Numero de puerto invalido: %s\n" % repr(options.port))
        parser.print_help()
        sys.exit(1)

    server = Server(options.address, port, options.datadir)
    server.serve()


if __name__ == "__main__":
    main()
