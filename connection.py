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
        self.connected = True
        self.buffer = ''
        # data que entra
        # data que sale
        self.send_buffer = b''

    def quit_handler(self, _):
        print("Client requested to quit.")
        self.connected = False
        self.socket.close()
        return CODE_OK, "OK"

    def get_file_listing_handler(self, args):
        list = os.listdir(self.dir)
        self.buffer = "0 OK\r\n"
        
        for l in list:
            try:
                l.encode("ascii")
                self.buffer += f"{l}\r\n"
            except UnicodeEncodeError:
                print(f"Nombre de archivo no ASCII omitido: {l}")
        
        try:
            self.socket.sendall((self.buffer + EOL).encode("ascii"))
        except Exception as e:
            print(f"Error al enviar datos: {e}")
        return CODE_OK, "OK"
    
    def get_metadata_handler(self, args):
    # Verificar número de argumentos
        if len(args) != 1:
            self.socket.sendall(f"{INVALID_ARGUMENTS} Invalid arguments\r\n".encode("ascii"))
            return INVALID_ARGUMENTS

        # Construir la ruta completa del archivo
        filepath = os.path.join(self.dir, args[0])

        # Verificar si el archivo existe
        if not os.path.isfile(filepath):
            self.socket.sendall(f"{FILE_NOT_FOUND} File not found\r\n".encode("ascii"))
            return FILE_NOT_FOUND

        try:
            # Obtener tamaño del archivo
            size = os.path.getsize(filepath)

            # Debug: Mostrar en el servidor qué tamaño se está obteniendo
            print(f"DEBUG: Tamaño de '{filepath}' = {size} bytes")

            # Enviar la respuesta con el formato correcto
            response = f"{CODE_OK} OK\r\n{str(size)}\r\n"

            # Debug: Mostrar qué se enviará
            print(f"DEBUG: Enviando respuesta -> {repr(response)}")

            self.socket.sendall(response.encode("ascii"))

            return CODE_OK, "OK"

        except OSError as e:
            print(f"Error al obtener metadatos: {e}")
            self.socket.sendall(f"{INTERNAL_ERROR} Internal error\r\n".encode("ascii"))
            return INTERNAL_ERROR

    
    
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

            # revisar
            if not command:
                self.socket.send(f"{BAD_REQUEST} invalid request format\n".encode("ascii"))
                continue
                # me parece que es un break
            
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
                self.socket.send(f"{INVALID_COMMAND} unknown command\n".encode("ascii"))
                continue