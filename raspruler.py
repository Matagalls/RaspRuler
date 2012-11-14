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
import gobject

import raspberryPi_cln as RpBy
import constants as K
import config_file_manager as CFM

EMPTY = " -- "
NO = "NO"
YES = "YES"

class MainWindow(gtk.Window):


    def completeInformation(self):
        """ With the GUI created, filling it with data. """
        self.setStructuralInfo()


    def initConnectionWithClient(self):
        """ Try to set a connection with the RpBy server. """
        self.client = RpBy.rasp_cln()


    def setStructuralInfo(self):
        """ Set all the structural info coming from the server. """
        
        self.dict_struct_info = self.client.getStruturalInfo()

        if self.dict_struct_info is not False:
            self.label_OS_value.set_text(self.dict_struct_info["os"])
            self.label_cpu_value.set_text(self.dict_struct_info["cpu"])
            self.label_ram_value.set_text(K.memoryResizer(self.dict_struct_info["ram_total"]))

  #          self.label_amule_installed.set_text(K.strBoolean(self.dict_struct_info["amule_installed"]))
  #          self.label_torrent_installed.set_text(K.strBoolean(self.dict_struct_info["torrent_installed"]))
  #          self.label_git_installed.set_text(K.strBoolean(self.dict_struct_info["git_installed"]))
  #          self.label_owncloud_installed.set_text(K.strBoolean(self.dict_struct_info["owncloud_installed"]))


    def get_main_menu(self, window):
        accel_group = gtk.AccelGroup()

        item_factory = gtk.ItemFactory(gtk.MenuBar, "<main>", accel_group)

        item_factory.create_items(self.menu_items)

        window.add_accel_group(accel_group)
        self.item_factory = item_factory

        return item_factory.get_widget("<main>")

    
    def __init__(self):
        """ Painfully long creation of the GUI. Please don't cry blood. """

        self.initConnectionWithClient()

        self.main_win = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.main_win.set_title("RaspRuler")   
        self.main_win.set_position(gtk.WIN_POS_CENTER)
        self.main_win.set_size_request(640, 500)     
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

        self.table_general_info = gtk.Table(4, 2, False)

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
        self.table_general_info.attach(self.frame_hardware_info, 0, 2, 0, 1, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)

        # Software frame

        self.frame_software_info = gtk.Frame("General Software Information")

        self.table_software_info = gtk.Table(1, 1, False)

        self.label_OS_title = gtk.Label("Operating system:")
        self.label_OS_value = gtk.Label(EMPTY)

        self.table_software_info.attach(self.label_OS_title, 0, 1, 0, 1, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
        self.table_software_info.attach(self.label_OS_value, 1, 2, 0, 1, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)

        self.frame_software_info.add(self.table_software_info)
        self.table_general_info.attach(self.frame_software_info, 0, 2, 1, 2, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)


        # Connection frame

        self.frame_connection_info = gtk.Frame("Connection with server")

        self.table_connection_info = gtk.Table(2, 1, False)

             # Connection label

        self.label_connection_title = gtk.Label("Connection:")

        if self.client.connection:
            self.label_connection_value = gtk.Label("Connected")
        else:   
            self.label_connection_value = gtk.Label("Not Connected")

            # Ip label

        self.label_connection_ip_server_title = gtk.Label("Server IP:")
        self.label_connection_ip_server_value = gtk.Label(self.client.config_info["server_ip"])

        self.table_connection_info.attach(self.label_connection_title, 0, 1, 0, 1, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
        self.table_connection_info.attach(self.label_connection_value, 1, 2, 0, 1, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
        self.table_connection_info.attach(self.label_connection_ip_server_title, 0, 1, 1, 2, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
        self.table_connection_info.attach(self.label_connection_ip_server_value, 1, 2, 1, 2, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)

        self.frame_connection_info.add(self.table_connection_info)
        self.table_general_info.attach(self.frame_connection_info, 0, 2, 2, 3, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)


        # Halt button and restart button
        self.button_halt = gtk.Button("Halt Server")
        self.button_halt.connect("clicked",self.halt_request)
        self.button_restart = gtk.Button("Restart Server")
        self.button_restart.connect("clicked",self.reboot_request)
        self.table_general_info.attach(self.button_halt, 0, 1, 3, 4, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
        self.table_general_info.attach(self.button_restart, 1, 2, 3, 4, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)


        self.label_title_slide_info = gtk.Label("General information")
        self.notebook.append_page(self.table_general_info, self.label_title_slide_info)



        ##### Slide page about services
        self.frame_services = gtk.Frame("Services overview")

        self.createServicesTable()

        self.frame_services.add(self.table_services)

#        self.label_title_slide_services = gtk.Label("Services")
#        self.notebook.append_page(self.frame_services, self.label_title_slide_services)

        # Add new service

        self.frame_add_service = gtk.Frame("Add service")
        self.table_add_service = gtk.Table(2, 5, False)
        self.label_new_service_name = gtk.Label("New service name:")
        self.label_new_service_daemon_name = gtk.Label("New service daemon name:")
        self.label_new_service_port = gtk.Label("New service port:")
        self.button_add_new_service = gtk.Button("Add new service")
        self.entry_new_service_daemon_name = gtk.Entry()
        self.entry_new_service_name = gtk.Entry()
        self.entry_new_port_name = gtk.Entry()

        self.table_add_service.attach(self.label_new_service_name, 0, 1, 0, 1, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
        self.table_add_service.attach(self.entry_new_service_name, 1, 2, 0, 1, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
        self.table_add_service.attach(self.label_new_service_port, 0, 1, 1, 2, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
        self.table_add_service.attach(self.entry_new_port_name, 1, 2, 1, 2, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
        self.table_add_service.attach(self.label_new_service_daemon_name, 0, 1, 2, 3, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
        self.table_add_service.attach(self.entry_new_service_daemon_name, 1, 2, 2, 3, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
        self.table_add_service.attach(self.button_add_new_service, 1, 2, 3, 4, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)

        self.frame_add_service.add(self.table_add_service)

        self.vbox_services = gtk.VBox(gtk.FALSE, 1)
        self.vbox_services.set_border_width(1)

        self.vbox_services.pack_start(self.frame_services)
        self.vbox_services.pack_start(self.frame_add_service)


        self.label_title_slide_services = gtk.Label("Services")
        self.notebook.append_page(self.vbox_services, self.label_title_slide_services)


        ##### Slide about resources
        self.frame_server_resources = gtk.Frame("Server Resources")
        self.table_server_resources = gtk.Table(2, 2, False)

        self.label_ram_title = gtk.Label("Ram memory used: ")
        self.label_ram_total_and_used = gtk.Label(EMPTY)
        self.label_hd_title = gtk.Label("Hdd space: ")
        self.label_hd_total_and_used = gtk.Label(EMPTY)

        self.table_server_resources.attach(self.label_ram_title, 0, 1, 0, 1, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
        self.table_server_resources.attach(self.label_ram_total_and_used, 1, 2, 0, 1, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
        self.table_server_resources.attach(self.label_hd_title, 0, 1, 1, 2, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
        self.table_server_resources.attach(self.label_hd_total_and_used, 1, 2, 1, 2, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)




        self.frame_server_resources.add(self.table_server_resources)

        self.label_title_slide_server_resources = gtk.Label("Server Resources")
        self.notebook.append_page(self.frame_server_resources, self.label_title_slide_server_resources)


        ##### Slide about backup's
        self.frame_backup = gtk.Frame("Backup")


        self.label_title_slide_backup = gtk.Label("Backup")
        self.notebook.append_page(self.frame_backup, self.label_title_slide_backup)


        ##### Slide about change parameters
        self.frame_parameters = gtk.Frame("Parameters")

        self.table_parameters = gtk.Table(1, 2, False)

        self.label_par_server_ip = gtk.Label("Server IP")
        self.entry_par_server_ip = gtk.Entry()
        self.button_apply_par_modifications = gtk.Button("Apply modifications")
        self.button_apply_par_modifications.connect("clicked",self.apply_par_modifications)

        self.table_parameters.attach(self.label_par_server_ip, 0, 1, 0, 1, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
        self.table_parameters.attach(self.entry_par_server_ip, 1, 2, 0, 1, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
        self.table_parameters.attach(self.button_apply_par_modifications, 1, 2, 1, 2, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)


        self.frame_parameters.add(self.table_parameters)
        self.label_title_slide_parameters = gtk.Label("Parameters")
        self.notebook.append_page(self.frame_parameters, self.label_title_slide_parameters)


        ##### End of slices

        self.main_win.show_all()    
        self.completeInformation()

        ##### Add timer
        gobject.timeout_add_seconds(5, self.timedFunctions)

    
    def createServicesTable(self):
        """ Generate a table from the services read in the config file. """

        self.table_services = gtk.Table(5, len(self.client.services) + 1, False)

        # Add menu in the top of the table
        self.label_top_table_name = gtk.Label("Name")
        self.label_top_table_working = gtk.Label("Working")
        self.label_top_table_onoff = gtk.Label("ON/OFF")
        self.label_top_table_website = gtk.Label("Launch Website")
        self.label_top_table_edit = gtk.Label("Edit")
        self.table_services.attach(self.label_top_table_name, 0, 1, 0, 1, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
        self.table_services.attach(self.label_top_table_working, 1, 2, 0, 1, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
        self.table_services.attach(self.label_top_table_onoff, 2, 3, 0, 1, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
        self.table_services.attach(self.label_top_table_website, 3, 4, 0, 1, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
        self.table_services.attach(self.label_top_table_edit, 4, 5, 0, 1, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)

        i = 1
        self.list_services = list()
        for service in self.client.services:
            row = list()
            row.append(gtk.Label(service.name))
            row.append(gtk.Label())
            row.append(gtk.Button("Start/Stop"))
            if service.web_interface:
                row.append(gtk.Button("Launch Website"))
            row.append(gtk.Button("Edit"))



            self.list_services.append(row)

            self.table_services.attach(row[0], 0, 1, 0+i, 1+i, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
            self.table_services.attach(row[1], 1, 2, 0+i, 1+i, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
            self.table_services.attach(row[2], 2, 3, 0+i, 1+i, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
            self.table_services.attach(row[3], 3, 4, 0+i, 1+i, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)
            self.table_services.attach(row[4], 4, 5, 0+i, 1+i, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=6, ypadding=6)



########## Button attending Functions

    def halt_request(self, widget, data=None):
        answer = self.client.halt_request()
        if answer == "no_superuser":
            self.dialog_no_su_server()

    def reboot_request(self, widget, data=None):
        answer = self.client.reboot_request()
        if answer == "no_superuser":
            self.dialog_no_su_server()

    def apply_par_modifications(self, widget, data=None):
        # Modify IP, if needed
        new_ip = self.entry_par_server_ip.get_text()
        is_ip_valid = K.isValidIPv4(new_ip)
        if is_ip_valid and new_ip != self.client.config_info["server_ip"]:
            self.client.modifyConfigParameter("server_ip", new_ip)
            self.client.resetConnection()
            self.updatAll()
        elif new_ip == self.client.config_info["server_ip"]:
            logging.info("Same IP; not applying changes")
        else:
            self.dialog_ip_adress_incorrect()

########## </Button attending Functions>

########## DialogMessage

    def dialog_no_su_server(self):
        md = gtk.MessageDialog(self, 
            gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_WARNING, 
            gtk.BUTTONS_CLOSE, "Server hasn't superuser privilegies.")
        md.run()
        md.destroy()

    def dialog_ip_adress_incorrect(self):
        md = gtk.MessageDialog(self, 
            gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_WARNING, 
            gtk.BUTTONS_CLOSE, "IPv4 incorrect.")
        md.run()
        md.destroy()

########## </DialogMessage>

    def on_quit(self, widget, data=None):
        """ Closing function. """
        if self.client.connection:
            self.client.closeConnection()
        gtk.main_quit()


    def updateVariableInfo(self):
        """ Update all the variable info. """
        if self.client.connection:
            def createStringWithPercents(value1, total):
                """ Return a string with 2 values and the percent. """
                return K.memoryResizer(value1) + " of " + K.memoryResizer(total)\
                         + " used (" + str(100*int(value1)/int(total)) + "%)" 


            dict_info = self.client.updateVariableInfo()

            string = createStringWithPercents(dict_info["ram_used"],self.dict_struct_info["ram_total"])
            self.label_ram_total_and_used.set_text(string)


    def timedFunctions(self):
        """ Bundle all the timed functions. """
        #self.updateVariableInfo()
        return True


    def updatAll(self):
        """ Update all the labels that may been changed. """
        # Label connected
        if self.client.connection:
            self.label_connection_value.set_text("Connected")
        else:   
            self.label_connection_value.set_text("Not Connected")
        # Label server IP
        self.label_connection_ip_server_value.set_text(self.client.config_info["server_ip"])
        #self.main_win.show_all()  

if __name__ == "__main__":

    parametres = set(sys.argv[1:])

    if len(parametres & {"-d", "-debug", "--debug"}) > 0:   
        logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s')
        logging.info('Logger initiated in DEBUG level')
    else:
        logging.basicConfig(format='%(levelname)s:%(message)s')

    MainWindow()
    gtk.main()
