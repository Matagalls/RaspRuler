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

import pygtk
pygtk.require("2.0")
import gtk
import sys
import logging

import RaspberryPi_cln as RpBy
import constants as K

EMPTY = " -- "

class MainWindow:


    def completeInformation(self):
        """ With the GUI created, filling it with data. """
        self.setStructuralInfo()


    def initConnectionWithClient(self):
        """ Try to set a connection with the RpBy server. """

        self.client = RpBy.rasp_cln()


    def setStructuralInfo(self):
        """ Set all the structural info coming from the server. """
        
        dict_struct_info = self.client.getStruturalInfo()

        self.label_OS_value.set_text(dict_struct_info["os"])
        self.label_cpu_value.set_text(dict_struct_info["cpu"])

        self.label_ram_value.set_text(K.memoryResizer(dict_struct_info["ram_total"]))


    def get_main_menu(self, window):
        accel_group = gtk.AccelGroup()

        item_factory = gtk.ItemFactory(gtk.MenuBar, "<main>", accel_group)

        item_factory.create_items(self.menu_items)

        window.add_accel_group(accel_group)
        self.item_factory = item_factory

        return item_factory.get_widget("<main>")

    
    def __init__(self):

        self.initConnectionWithClient()

        self.main_win = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.main_win.set_title("RaspRuler")   
        self.main_win.set_position(gtk.WIN_POS_CENTER)
        self.main_win.set_size_request(500, 400)     
        self.main_win.connect("destroy", self.on_quit)
        self.main_win.set_border_width(10)
        
        self.notebook = gtk.Notebook()

        ##### Menu

        self.menu_items = (
            ("/File", None, None, 0, "<Branch>"),
            ("/File/Start connection", None, None, 0, None),
            ("/File/Close connection", None, None, 0, None),
            ("/File/Restart connection", None, None, 0, None),
            ("/File/Exit", None, self.on_quit, 0, None),
            ("/Help", None, None, 0, "<Branch>"),
            ("/Help/About RaspRuler", None, None, 0, None),
            )            

        self.main_vbox = gtk.VBox(gtk.FALSE, 1)
        self.main_vbox.set_border_width(1)
        self.main_win.add(self.main_vbox)

        self.menubar = self.get_main_menu(self.main_win)

        self.main_vbox.pack_start(self.menubar, gtk.FALSE, gtk.TRUE, 0)


        self.main_vbox.pack_start(self.notebook)
        self.notebook.set_tab_pos(gtk.POS_TOP)

        ##### Slide page about state of the raspberry

        self.table_general_info = gtk.Table(3, 1, False)

        # Hardware frame
        self.frame_hardware_info = gtk.Frame("General Hardware Information")

        self.table_hardware_info = gtk.Table(2, 2, False)

        self.label_ram_title = gtk.Label("RAM memory installed:")
        self.label_ram_value = gtk.Label(EMPTY)
        self.label_cpu_title = gtk.Label("CPU :")
        self.label_cpu_value = gtk.Label(EMPTY)

        self.table_hardware_info.attach(self.label_ram_title, 0, 1, 0, 1, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
        self.table_hardware_info.attach(self.label_ram_value, 1, 2, 0, 1, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
        self.table_hardware_info.attach(self.label_cpu_title, 0, 1, 1, 2, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
        self.table_hardware_info.attach(self.label_cpu_value, 1, 2, 1, 2, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)

        self.frame_hardware_info.add(self.table_hardware_info)
        self.table_general_info.attach(self.frame_hardware_info, 0, 1, 0, 1, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)

        # Software frame

        self.frame_software_info = gtk.Frame("General Software Information")

        self.table_software_info = gtk.Table(1, 1, False)

        self.label_OS_title = gtk.Label("Operating system:")
        self.label_OS_value = gtk.Label(EMPTY)

        self.table_software_info.attach(self.label_OS_title, 0, 1, 0, 1, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
        self.table_software_info.attach(self.label_OS_value, 1, 2, 0, 1, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)

        self.frame_software_info.add(self.table_software_info)
        self.table_general_info.attach(self.frame_software_info, 0, 1, 1, 2, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)


        # Connection frame

        self.frame_connection_info = gtk.Frame("Connection with the server")

        self.table_connection_info = gtk.Table(1, 1, False)

        self.label_connection_title = gtk.Label("Connection:")

        if self.client.connection:
            self.label_connection_value = gtk.Label("Connected")
        else:   
            self.label_connection_value = gtk.Label("Not Connected")

        self.table_connection_info.attach(self.label_connection_title, 0, 1, 0, 1, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
        self.table_connection_info.attach(self.label_connection_value, 1, 2, 0, 1, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)

        self.frame_connection_info.add(self.table_connection_info)
        self.table_general_info.attach(self.frame_connection_info, 0, 1, 2, 3, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)



        self.label_title_slide_info = gtk.Label("General information")
        self.notebook.append_page(self.table_general_info, self.label_title_slide_info)



        ##### Slide page about services
        self.frame_services = gtk.Frame("Services overview")
        self.table_services = gtk.Table(4, 5, False)

        # Amule
        self.label_amule_title = gtk.Label("Amule")
        self.label_amule_installed = gtk.Label(EMPTY)
        self.label_amule_running = gtk.Label(EMPTY)
        self.button_amule_disable = gtk.Button("Disable")
        self.button_amule_launch_website = gtk.Button("Launch Website")

        self.table_services.attach(self.label_amule_title,           0, 1, 0, 1, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
        self.table_services.attach(self.label_amule_installed,       1, 2, 0, 1, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
        self.table_services.attach(self.label_amule_running,         2, 3, 0, 1, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
        self.table_services.attach(self.button_amule_disable,        3, 4, 0, 1, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
        self.table_services.attach(self.button_amule_launch_website, 4, 5, 0, 1, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)

        # Torrent
        self.label_torrent_title = gtk.Label("uTorrent")
        self.label_torrent_installed = gtk.Label(EMPTY)
        self.label_torrent_running = gtk.Label(EMPTY)
        self.button_torrent_disable = gtk.Button("Disable")
        self.button_torrent_launch_website = gtk.Button("Launch Website")

        self.table_services.attach(self.label_torrent_title,           0, 1, 1, 2, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
        self.table_services.attach(self.label_torrent_installed,       1, 2, 1, 2, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
        self.table_services.attach(self.label_torrent_running,         2, 3, 1, 2, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
        self.table_services.attach(self.button_torrent_disable,        3, 4, 1, 2, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
        self.table_services.attach(self.button_torrent_launch_website, 4, 5, 1, 2, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)

        # apache / owncloud
        self.label_owncloud_title = gtk.Label("owncloud")
        self.label_owncloud_installed = gtk.Label(EMPTY)
        self.label_owncloud_running = gtk.Label(EMPTY)
        self.button_owncloud_disable = gtk.Button("Disable")
        self.button_owncloud_launch_website = gtk.Button("Launch Website")

        self.table_services.attach(self.label_owncloud_title,           0, 1, 2, 3, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
        self.table_services.attach(self.label_owncloud_installed,       1, 2, 2, 3, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
        self.table_services.attach(self.label_owncloud_running,         2, 3, 2, 3, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
        self.table_services.attach(self.button_owncloud_disable,        3, 4, 2, 3, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
        self.table_services.attach(self.button_owncloud_launch_website, 4, 5, 2, 3, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)

        # git
        self.label_git_title = gtk.Label("git")
        self.label_git_installed = gtk.Label(EMPTY)

        self.table_services.attach(self.label_git_title,           0, 1, 3, 4, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
        self.table_services.attach(self.label_git_installed,       1, 2, 3, 4, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)





        self.frame_services.add(self.table_services)

        self.label_title_slide_services = gtk.Label("Services")
        self.notebook.append_page(self.frame_services, self.label_title_slide_services)

        self.main_win.show_all()

    
        self.completeInformation()
    

    # Ahora se define el método "on_quit" que destruye la aplicación
    def on_quit(self, widget, data=None):

        if self.client.connection:
            self.client.closeConnection()

        gtk.main_quit()


    def service_amule_disable(self, widget):
        print "service_amule_disable"



if __name__ == "__main__":

    parametres = set(sys.argv[1:])

    if len(parametres & {"-d", "-debug", "--debug"}) > 0:   
        logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s')
        logging.info('Logger iniciat amb nivell DEBUG')
    else:
        logging.basicConfig(format='%(levelname)s:%(message)s')

    MainWindow()
    gtk.main()
