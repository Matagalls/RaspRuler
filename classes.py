#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
##                          Raspberry Pi GUI Client                          ##
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

class service():

    def __init__(self, name, name_process, web_interface, port):
        self.name = name
        self.name_process = name_process
        self.web_interface = web_interface
        self.port = port


class backup():

    def __init__(self, origin_dir, origin_mach, destiny_dir, destiny_mach):
        self.origin_directory = origin_dir
        self.origin_machine = origin_mach
        self.destiny_directory = destiny_dir
        self.destiny_machine = destiny_mach 
