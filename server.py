#!/usr/bin/env python
# encoding: utf-8
# Revisión 2019 (a Python 3 y base64): Pablo Ventura
# Revisión 2014 Carlos Bederián
# Revisión 2011 Nicolás Wolovick
# Copyright 2008-2010 Natalia Bidart y Daniel Moisset
# $Id: server.py 656 2013-03-18 23:49:11Z bc $

import optparse
import socket
from connection import Connection
from constants import *
import sys
import select


class Server():
    """
    El servidor, que crea y atiende el socket en la dirección y puerto
    especificados donde se reciben nuevas conexiones de clientes.
    """

    def __init__(self, addr=DEFAULT_ADDR, port=DEFAULT_PORT, directory=DEFAULT_DIR):
        self.dir = directory 
        self.port = port
        self.addr = addr
        self.poller = None
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print("Serving %s on %s:%s." % (directory, addr, port))
        clients = {}

    def serve(self):
        """
        Loop principal del servidor. Se acepta una conexión a la vez
        y se espera a que concluya antes de seguir.
        """
        self.s.bind((self.addr, self.port))
        self.s.listen()
        print("Servidor esperando conexiones...")
        
        # esperar eventos en múltiples descriptores de archivo
        self.poller = select.poll()
        # avisame cuando haya datos por leer "pollin"
        self.poller.register(self.s, select.POLLIN)
        # 
        
        # el acep
        # conn, addr = self.s.accept()
        #   
        
        while True:
            events = self.poller.poll() # espera eventos
            for sock_fd, event in events:
                if event & select.POLLOUT:
                    # ya lo tengo guardado y quiere escribir
                    pass
                elif event & select.POLLIN:
                    if sock_fd == self.s.fileno(): 
                        new_client_socket, addr = self.s.accept()
                        new_client_socket.setblocking(False) # no bloquea cuando uso recv
                        self.poller.register(new_client_socket, select.POLLIN)
                        self.clients[new_client_socket.fileno()] = Connection(new_client_socket, self.dir)
                    else:
                        # ya tengo guardado y quiere leer
                        pass    

def main():
    """Parsea los argumentos y lanza el server"""

    parser = optparse.OptionParser()
    parser.add_option(
        "-p", "--port",
        help="Número de puerto TCP donde escuchar", default=DEFAULT_PORT)
    parser.add_option(
        "-a", "--address",
        help="Dirección donde escuchar", default=DEFAULT_ADDR)
    parser.add_option(
        "-d", "--datadir",
        help="Directorio compartido", default=DEFAULT_DIR)

    options, args = parser.parse_args()
    if len(args) > 0:
        parser.print_help()
        sys.exit(1)
    try:
        port = int(options.port)
    except ValueError:
        sys.stderr.write(
            "Numero de puerto invalido: %s\n" % repr(options.port))
        parser.print_help()
        sys.exit(1)

    server = Server(options.address, port, options.datadir)
    server.serve()


if __name__ == '__main__':
    main()
