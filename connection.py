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

class Connection():
    """
    Conexión punto a punto entre el servidor y un cliente.
    Se encarga de satisfacer los pedidos del cliente hasta
    que termina la conexión.
    """

    def __init__(self, socket, directory):
        self.socket = socket
        self.dir = directory
        self.commands = {
            "get_file_listing": "arg, fun",
            "get_metadata": "arg, fun",
            "get_slice": "arg, fun",
            "quit": "arg, fun",
        }
        self.quit = False
        self.running = True
        # data que entra
        self.data_acc = ''
        # data que sale
        self.send_buffer = b''

    def quit_handler(self):
        print("Client requested to quit.")
        self.quit = True
        return CODE_OK, "OK"

    def get_file_listing_handler(self):
        pass
    
    def get_metadata_handler(self, args):
        pass
    
    def get_slice_handler(self, args):
        pass

    def handle(self):
        """
        Atiende eventos de la conexión hasta que termina.
        """
        # muy verde todavia
        while self.running:
            # procesar el input y dependiendo de lo que agarres mandas un handle
            try: 
                input = self.socket.recv().decode("ascii")
            except:
                pass
            match = re.match(PATTERN, input)
            cmd = match.group(1)
            arg = match.group(2)