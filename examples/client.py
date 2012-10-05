#!/usr/bin/env python
# -*- coding: utf-8 -*-

# diguito69

import socket

# Ejemplo de un socket cliente simple.

def main():
    # Creamos el socket y lo conectamos.
    s = socket.socket()  
    s.connect(("localhost", 6969))

    while 1:
        # Espera entrada por teclado.
        mensaje = raw_input("-> ")
        # Le envía el mensaje al server.
        s.send(mensaje)
        print "Mensaje enviado."
        # Si el mensaje es "quit" termina el bucle.
        if mensaje == "quit":
            break 
   
    print "Cerrando..."
    # Cerramos el socket
    s.close()  

if __name__ == "__main__":
    main()
