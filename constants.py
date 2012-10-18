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
PORT = 3658
# All the commands between the client and the server.
COMMANDS = {"free_space_disk","quit","get_structural_info",\
            "update_variable_info","halt"}

UNKNOWN_COMMAND = "Unknown_command"


def serializeDict(dictionary):
    """ Convert a dict into a string to be send through a socket. """
    dict_serialized = ""
    return str(dictionary)



def unserializeDict(string):
    """ Convert a dict into a string to be send through a socket. """
    return ast.literal_eval(string)


def memoryResizer(memory):
    """ Adjust memory size in the correct units. Memory parameter in Kbyts. """

    memory = int(memory)
    if memory / 1024 > 1:
        memory_int = memory / 1024
        memory_dec = memory % 1024
        units = "Mb"
        if memory_int / 1024 > 1:
            memory = memory_int
            memory_int = memory / 1024
            memory_dec = memory % 1024
            units = "Gb"

    else:
        units = "Kb"

    return str(memory_int) + "." + str(memory_dec)[:2] + " " + units


def strBoolean(bool_value):
    """ Convert a boolean value into a string in order to put it in a label """

    if bool_value is True:
        return "Yes"
    elif bool_value is False:
        return "No"
    else:
        return "not_implemented"

















