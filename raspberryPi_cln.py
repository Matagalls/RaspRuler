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

import constants as K

COMMANDS = K.COMMANDS

VERSION = "0.0.1"
TIMEOUT = 2

class rasp_cln():

    def __init__(self, server_ip):

        self.connection = False
        self.server_ip = server_ip

        self.setConnection()


    def closeConnection(self):
        logging.debug("Closing connection")
        self.socket.send("quit")
        self.socket.close()  


    def setConnection(self):
        """ Create connection """
        self.socket = socket.socket()
        if self.connection is not True:
            try:
                self.socket.connect((self.server_ip, K.PORT))
                self.connection = True
                logging.debug("Connection established")
                self.socket.settimeout(TIMEOUT)
            except:
                self.connection = False
                logging.warning("Can't found server. Connection not established")
                self.socket.close()

        else:
            logging.info("Connection already set. Ignoring ... ")

    
    def getStruturalInfo(self):
        """ Request all the structural info """

        if self.connection:
            dict_info = self.senderAndReciverManager("get_structural_info")
            if dict_info is not False:
                return dict_info
            else:
                return False
        else:
            return False

    
    def senderAndReciverManager(self, command):
        """ Manage sending petitions over the socket and reading them.
            Return what server send if all the process succeed, and False
            if something had gone wrong. 
            
            Return a dict with all the data. """

        if self.connection:
            if command in COMMANDS:
                self.socket.send(command)
                answer = self.socket.recv(1000)

                if answer is not None:
                    if answer == K.UNKNOWN_COMMAND:
                        logging.warning("Server can't understant last command: %s", command)
                        return False
                    else:
                        if command == "get_structural_info" or command == "update_variable_info":
                            return K.unserializeDict(answer)
                        else:
                            return answer
                else:
                    logging.warning("Recived empty answer from command: %s", command)
                    return False
            else:
                logging.warning('Not sending unknown command: %s. Ingnoring', command)
                return False
        else:
            logging.warning("No connection established")
            return False


    def updateVariableInfo(self):
        """ Refresh some variable info. """
        return self.senderAndReciverManager("update_variable_info")   


    def halt_request(self):
        answer = self.senderAndReciverManager("halt")
        if answer == True:
            print "xapant ... "
        elif answer == "no_superuser":
            logging.warning("Server process have no permission to halt.")


    def reboot_request(self):
        answer = self.senderAndReciverManager("reboot")
        if answer == True:
            print "rebotant ... "
        elif answer == "no_superuser":
            logging.warning("Server process have no permission to reboot.")    



if __name__ == "__main__":

    # Check OS
    if (os.name == "posix"):
        logging.info("OS Linux")
    elif (os.name == "nt"):
        logging.error("OS Windows not suported. Exiting ...")
        sys.exit(-1)
    else:
        logging.error("Unknown OS. Exiting ...")
        sys.exit(-1)

    client   = rasp_cln()
        
