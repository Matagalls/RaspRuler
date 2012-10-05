#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
##                             Raspberry Pi Client                           ##
###############################################################################

#
#  Copyright 2012 Àlex Cors Bardolet
#
#  This file is part of RaspRuler.
#
#  RaspRuler is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  RaspRuler is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with RaspRuler.  If not, see <http://www.gnu.org/licenses/>.
#

import socket
import logging
import sys

VERSION = "0.0.1"
PORT = 3658
TIMEOUT = 2

class rasp_cln():

    def __init__(self):

        # Connection stuff
        self.socket = socket.socket()  # Not safe
        self.socket.connect(("localhost", PORT))
        self.socket.settimeout(TIMEOUT)

        # Data 

        self.bucle()


    def bucle(self):

        while 1:
            mensaje = raw_input("-> ")
            self.socket.send(mensaje)

            answer = self.socket.recv(1000)
            
            if answer is not None:
                if answer == "Unknown_command":
                    logging.warning("Server can't understant last command")
                else:
                    print answer
            else:
                logging.warning('Recived empty answer')

            if mensaje == "quit":
                break 
       
        self.socket.close()  



if __name__ == "__main__":

    parametres = set(sys.argv[1:])

    if len(parametres & {"-d", "-debug", "--debug"}) > 0:   
        logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s')
        logging.info('Logger iniciat amb nivell DEBUG')
    else:
        logging.basicConfig(format='%(levelname)s:%(message)s')

    client = rasp_cln()
        
