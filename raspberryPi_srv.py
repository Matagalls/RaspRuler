#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
##                             Raspberry Pi server                           ##
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
import os

VERSION = "0.0.1"
PORT = 3658
MAX_USERS = 1

COMMANDS = {"free_space_disk","quit"}

class rasp_srv():

    def __init__(self):

        # Socket related stuff              

        self.wait()

    def wait(self):

        while 1:

            self.auxSocket = socket.socket()
            self.auxSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.auxSocket.bind(("localhost", PORT))
            logging.info('Waiting for clinets to connect ...')
            self.auxSocket.listen(MAX_USERS)

            self.socketClient, clientInfo = self.auxSocket.accept()
            self.clientAddress = clientInfo[0]
            self.clientPort = clientInfo[1]
            logging.info('Client from %s connected and accepted.', self.clientAddress)

            while 1:
                command = self.socketClient.recv(1000)
                if command in COMMANDS:

                    if command == "free_space_disk":
                        answer = self.getFreeHdSpace()

                    elif command == "quit":
                        break 

                else:
                    answer = "Unknown_command"
                    logging.warning('Recived unknown command: %s. Ingnoring', command)

                self.socketClient.send(answer)                

            logging.info('Closing sockets with %s', self.clientAddress)
            self.socketClient.close()
            self.auxSocket.close()


    def getAvailableHdSpace():
        """ Return all the available space in the HD, in Kb. """
        stats = os.statvfs('/')
        return str(stats[statvfs.F_BSIZE] * stats[statvfs.F_BAVAIL] / 1024)

    
    def getFreeHdSpace(self):
        """ Return the free space in the HD, in Kb. """
        s = os.statvfs('/')
        a = (s.f_bavail * s.f_frsize) / 1024 # Kb
        return str(a)


    def isAmuleInstalled():
        """ Check if amule is installed """
        if os.path.isfile("/etc/init-d/amule-daemon"):
            return True
        else:
            return False


    def isTransmissionInstalled():
        """ Check if transmission is installed """
        if os.path.isfile("/etc/init-d/transmission-daemon"):
            return True
        else:
            return False


    #def doBackUp



if __name__ == "__main__":

    parametres = set(sys.argv[1:])

    if len(parametres & {"-d", "-debug", "--debug"}) > 0:   
        logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s')
        logging.info('Logger iniciat amb nivell DEBUG')
    else:
        logging.basicConfig(format='%(levelname)s:%(message)s')
    server = rasp_srv()

