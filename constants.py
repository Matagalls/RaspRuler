#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
##                       Raspberry Pi Constants File                         ##
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

###############################################################################

import ast

VERSION = "0.0.1"

# All the commands between the client and the server.
COMMANDS = {"free_space_disk","quit","get_structural_info"}

UNKNOWN_COMMAND = "Unknown_command"


def serializeDict(dictionary):
    """ Convert a dict into a string to be send through a socket. """
    dict_serialized = ""

#    print dictionary

#    for tag, element in dictionary:
#        dict_serialized = dict_serialized + str(tag) + "=" + str(element) + "/"

    

#    return dict_serialized[:len(dict_serialized) - 1]

    return str(dictionary)



def unserializeDict(string):
    """ Convert a dict into a string to be send through a socket. """


#    list_aux = string.split("/")
#    for member in list_aux:
#        tag, element = member.split("=")
#        dict_unserialized[tag] = element

#    return dict_unserialized

    return ast.literal_eval(string)


def memoryResizer(memory):
    """ Adjust memory size in the correct units. Memory parameter in Kbytes. """

    memory = int(memory)

    if memory / 1024 > 1:
        memory = memory / 1024
        units = "Mb"
        if memory / 1024 > 1:
            memory = memory / 1024
            units = "Gb"

    else:
        units = "Kb"

    return str(memory) + " " + units


# NO DECIMALS!!!!!!!!!!!!!!!


















