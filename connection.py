# encoding: utf-8
# Revisión 2019 (a Python 3 y base64): Pablo Ventura
# Copyright 2014 Carlos Bederián
# $Id: connection.py 455 2011-05-01 00:32:09Z carlos $

import socket
from constants import *
from base64 import b64encode
import os
import base64

BUFFER_SIZE = 1024

class Connection:
    """
    Conexión punto a punto entre el servidor y un cliente.
    Se encarga de satisfacer los pedidos del cliente hasta
    que termina la conexión.
    """

    def __init__(self, socket, directory):
        self.socket = socket
        self.dir = directory
        self.connected = True
        self.buffer = ''
        self.command = {
            "get_file_listing": self.get_file_listing_handler,
            "get_metadata": self.get_metadata_handler,
            "get_slice": self.get_slice_handler,
            "quit": self.quit_handler
        }

    def quit_handler(self, _):
        self.connected = False
        self.send(CODE_OK)

    def get_file_listing_handler(self, _):
        list = os.listdir(self.dir)
        body = ""
        for l in list:
            try:
                l.encode("ascii")
                body += f"{l}{EOL}"
            except UnicodeEncodeError:
                return UnicodeEncodeError
        self.send(CODE_OK, body)
    
    def get_size(self, filepath:str) -> str:
        filepath = os.path.join(self.dir, filepath)
        try:
            size = os.path.getsize(filepath)
            return size
        except:
            if not os.path.isfile(filepath):
                return -1

    def get_metadata_handler(self, args: list[str]):
        if len(args) != 1:
            return INVALID_ARGUMENTS
        
        size = self.get_size(args[0])
        if size == -1:
            return FILE_NOT_FOUND
        
        self.send(CODE_OK, str(size))
    
    def get_slice_handler(self, args: list[str]):
        if len(args) != 3:
            return INVALID_ARGUMENTS

        filename, offset, size_cut = args

        try:
            offset = int(offset)
            size_cut = int(size_cut)
        except ValueError:
            return INVALID_ARGUMENTS

        if offset < 0 or size_cut < 0:
            return INVALID_ARGUMENTS

        size = self.get_size(filename)
        if size == -1:
            return FILE_NOT_FOUND

        if offset + size_cut > size:
            return BAD_OFFSET

        try:
            filepath = os.path.join(self.dir, filename)
            with open(filepath, "rb") as f:
                f.seek(offset)
                body = f.read(size_cut)
                
            body_base64 = base64.b64encode(body).decode("utf-8")
            self.send(CODE_OK, body_base64)
        except FileNotFoundError:
            return FILE_NOT_FOUND
        except OSError:
            return OSError
    
    def send(self, error_code: int, body:str = ""):
        """_summary_

        Args:
            error_code (_type_): index error message
            body (_type_): msg body for client
        
        send(0,"") -> se envia "0 OK\r\n"
        send(0,"1.txt\r\n2.txt\r\n") -> "0 OK\n\r1.txt\r\n2.txt\r\n\r\n"
        """
        prefix = f"{error_code} {error_messages[error_code]}{EOL}"
        res = f"{prefix}{body}{EOL}"
        self.socket.sendall(res.encode('ascii'))
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
                continue

            parts = command.split()
            if not parts:
                continue

            cmd = parts[0].lower()
            args = parts[1:]

            if cmd in self.command:
                print(f"cmd: {cmd}")
                print(f"args: {args}")
                try:
                    error_code = self.command[cmd](args)  # Ejecuta el comando

                    if valid_status(error_code):
                        self.send(error_code)

                        # Si el error es fatal, cerramos la conexión
                        if fatal_status(error_code):
                            self.connected = False

                except (OSError,Exception) as e:
                    print(f"Unexpected OS error: {e}")
                    self.send(INTERNAL_ERROR)
                    self.connected = False
            else:
                self.send(INVALID_COMMAND)

        self.socket.close()
