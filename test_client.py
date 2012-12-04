# Testing some aspects of the client

import pygtk
pygtk.require("2.0")
import gtk
import sys
import logging
import gobject

import raspberryPi_cln as RpBy
import constants as K
import config_file_manager as CFM

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s')

a = RpBy.rasp_cln()

a.setConnection()
a.setConnection()

a.getStruturalInfo()

a.closeConnection()


a.setConnection()
a.setConnection()
a.closeConnection()
