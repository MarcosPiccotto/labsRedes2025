# encoding: utf-8
# Revisión 2019 (a Python 3 y base64): Pablo Ventura
# Copyright 2014 Carlos Bederián
# $Id: connection.py 455 2011-05-01 00:32:09Z carlos $

import socket
from constants import *
from base64 import b64encode
import os
import re

BUFFER_SIZE = 1024
PATTERN = r"^(\w+)(?:\s[\w.-]+)*\r\n$"

class Connection:
    """
    Conexión punto a punto entre el servidor y un cliente.
    Se encarga de satisfacer los pedidos del cliente hasta
    que termina la conexión.
    """

    def __init__(self, socket, directory):
        self.socket = socket
        self.dir = directory
        self.command = {
            "get_file_listing": self.get_file_listing_handler,
            "get_metadata": self.get_metadata_handler,
            "get_slice": self.get_slice_handler,
            "quit": self.quit_handler
        }
        self.quit = False
        self.connected = True
        self.buffer = ''
        # data que entra
        # data que sale
        self.send_buffer = b''

    def quit_handler(self, _):
        print("Client requested to quit.")
        self.quit = True
        return CODE_OK, "OK"

    def get_file_listing_handler(self, args):
        list = os.listdir(self.dir)
        for l in list:
            self.buffer += l
        message = "Listado de archivos:"
        self.socket.sendall((message + EOL).encode("ascii"))
        return CODE_OK, "OK"
    
    def get_metadata_handler(self, args):
        pass
    
    def get_slice_handler(self, args):
        pass

    def _read_line(self):
        """Lee una línea del cliente."""
        while EOL not in self.buffer and self.connected:
            try:
                data = self.socket.recv(BUFFER_SIZE).decode("ascii")
                if not data:
                    self.connected = False
                    return ""
                self.buffer += data
            except (socket.error, UnicodeDecodeError):
                self.connected = False
                return ""
        
        if EOL in self.buffer:
            line, self.buffer = self.buffer.split(EOL, 1)
            return line.strip()
        return ""

    def handle(self):
        """
        Atiende eventos de la conexión hasta que termina.
        """
        while self.connected:
            command = self._read_line()

            if not command:
                self.socket.send(f"{BAD_REQUEST} invalid request format\n".encode())
                continue
            
            parts = command.split()
            if not parts:
                continue

            cmd = parts[0].lower()
            args = parts[1:]

            if cmd in self.command:
                print(f"cmd: {cmd}")
                print(f"args: {args}")
                self.command[cmd](args)
            else:
                self.socket.send(f"{INVALID_COMMAND} unknown command\n".encode())
                continue