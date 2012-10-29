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
import config_file_manager as CFM
import service

COMMANDS = K.COMMANDS

VERSION = "0.0.1"
TIMEOUT = 2

class rasp_cln():

    def __init__(self):

        self.connection = False

        self.services = list()
        self.config_file = CFM.ConfigFile()
        self.config_info = self.readConfigFile()

        self.setConnection()


    def closeConnection(self):
        logging.debug("Closing connection")
        self.socket.send("quit")
        self.socket.close()  


    def modifyConfigParameter(self, option, value):
        """ Modify only one parameter of the config file """

        self.config_file.modifyParameter(option, value)


    def analizeConfigFile(self, dict_config_file):
        """ Check for data integrity from config file. """

        config_info = {}

        if dict_config_file['server_ip_type'] == "static":
            config_info["server_ip"] = dict_config_file['server_ip']
        else:
            pass

        # process all the services
        for key in dict_config_file.keys():
            if key == "service":
                name, name_process, web_interface, port = dict_config_file[key].split("%")
                new_service = service.service(name, name_process, web_interface, port)
                self.services.append(new_service)

        return config_info


    def readConfigFile(self):
        """ Read the config file in order to get server ip and so on. """
        return self.analizeConfigFile(self.config_file.parseConfigFile())

    
    def reloadConfigFile(self):
        """ Read again config file. """
        self.config_info = self.readConfigFile()


    def resetConnection(self):
        """ Reset the connection reading againg config file. """

        if self.connection:
            self.socket.send("quit")
            self.socket.close()
            self.connection = False

        self.reloadConfigFile()
        self.setConnection()
        

    def setConnection(self):
        """ Create connection """
        self.socket = socket.socket()
        self.socket.settimeout(TIMEOUT)
        if self.connection is not True:
            try:
                self.socket.connect((self.config_info["server_ip"], K.PORT))
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
        if answer == "no_superuser":
            logging.warning("Server process have no permission to halt.")
        return answer


    def reboot_request(self):
        answer = self.senderAndReciverManager("reboot")
        if answer == "no_superuser":
            logging.warning("Server process have no permission to reboot.")    
        return answer


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

    client = rasp_cln()
        
