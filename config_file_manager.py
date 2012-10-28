#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
##                  Raspberry Pi Configuration File Manager                  ##
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

import logging
import sys

COMMENT_CHAR = '#'
OPTION_CHAR =  '='


class ConfigFile:


    def __init__(self):

        self.config_file_name = "config"
        self.file_exists = self.check_if_config_file_exists()


    def check_if_config_file_exists(self):

        try:
            f = open(self.config_file_name)
            f.close()
            file_exists = True
        except IOError as e:
            file_exists = False
            logging.error("Can't find config file. Exiting ... ")
            sys.exit(-1)

        return file_exists


    def parseConfigFile(self):
        options = {}
        f = open(self.config_file_name)
        for line in f:

            if COMMENT_CHAR in line: # Removing comments
                pass

            elif OPTION_CHAR in line: # Find lines with option=value
                option, value = line.split(OPTION_CHAR, 1)
                option = option.strip()
                value = value.strip()
                options[option] = value

        f.close()

        return options

