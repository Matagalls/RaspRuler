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

class test():

    def __init__(self):
        self._order_counter = 1

    def printOrder(self):
        print "!!!!!!!!!! Order number " + str(self._order_counter)
        self._order_counter += 1


test = test()

test.printOrder()
a = RpBy.rasp_cln()

test.printOrder()
a.setConnection()

test.printOrder()
a.setConnection()

test.printOrder()
a.getStruturalInfo()

test.printOrder()
a.closeConnection()

test.printOrder()
a.setConnection()

test.printOrder()
a.setConnection()

test.printOrder()
a.resetConnection()

test.printOrder()
a.closeConnection()
