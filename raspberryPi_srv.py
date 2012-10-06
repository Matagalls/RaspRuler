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
import subprocess

VERSION = "0.0.1"
PORT = 3658
MAX_USERS = 1

COMMANDS = {"free_space_disk","quit"}

class rasp_srv():

    def __init__(self, no_bucle):

        # Socket related stuff   
        self.info = {"os": "", 
                    "cpu": "",
                    "ram_total": "",
                    "ram_used": "",
                    "ram_free": "",
                    "amule_installed": "",
                    "torrent_installed": "",
                    "git_installed": "",
                    "owncloud_installed": "",
                    }           

        if not no_bucle:
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


    def getRamInfo(self):
        """ Get structural and dynamical info about Ram memory. """
    
        def cleanMemoString(memo_to_clean):
            """ Clean string """
            name, amount, aux_b = "", "", False
            unpacked = memo_to_clean.split(" ")
            for value in unpacked:
                if aux_b:
                    aux_b = False
                    if value[len(value) - 1:] == "\n":
                        name = value[:len(value) - 1]
                    else:
                        name = value

                if value[len(value) - 1:] == "k":
                    amount = value[:len(value) - 1]
                    aux_b = True
            
            return name, amount

        p = subprocess.Popen('top -b -n 1 | grep Mem', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        mem_line = p.stdout.readlines()[0]
        aux = mem_line.split(":")
        memories = aux[1].split(",")
        for memo in memories:
            name, amount = cleanMemoString(memo)
            if name == "total":
                self.info["ram_total"] = amount
            elif name == "used":
                self.info["ram_used"] = amount
            elif name == "free":
                self.info["ram_free"] = amount



    def getMachineName(self):
        p = subprocess.Popen('uname -m', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return p.stdout.readlines() # list!!!!!

    def getOsName(self):
        p = subprocess.Popen('uname -s', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return p.stdout.readlines()# list!!!!!

    def getAvailableHdSpace():
        """ Return all the available space in the HD, in Kb. """
        stats = os.statvfs('/')
        return str(stats[statvfs.F_BSIZE] * stats[statvfs.F_BAVAIL] / 1024)
    
    def getFreeHdSpace():
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

    def isTorrentInstalled():
        """ Check if transmission is installed """
        if os.path.isfile("/etc/init-d/transmission-daemon"):
            return True
        else:
            return False

    def isGitInstalled():
        return "no_implemented"

    def isOwncloudInstalled():
        return "no_implemented"


    def getStructuralInfo(self):
        """ Recopile all the info that not will change while the server
            is being executed. """

        self.info["amule_installed"] = self.isAmuleInstalled()
        self.info["torrent_installed"] = self.isTorrentInstalled()
        self.info["git_installed"] = self.isGitInstalled()
        self.info["owncloud_installed"] = self.isOwncloudInstalled()

        self.info["cpu"] = self.getMachineName()
        self.info["os"] = self.getOsName()
        self.getRamInfo()
    
            



    #def doBackUp



if __name__ == "__main__":

    parametres = set(sys.argv[1:])

    if len(parametres & {"-d", "-debug", "--debug"}) > 0:   
        logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s')
        logging.info('Logger iniciat amb nivell DEBUG')
    else:
        logging.basicConfig(format='%(levelname)s:%(message)s')

    if len(parametres & {"-n", "--no-bucle"}) > 0:   
        logging.basicConfig(format='%(levelname)s:%(message)s')
        no_bucle = True
    else:
        no_bucle = False

    server = rasp_srv(no_bucle)

