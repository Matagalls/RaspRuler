#!/usr/bin/env python
# -*- coding: utf-8 -*-

# diguito69

import socket

def main():
    # Creamos el socket.
    server = socket.socket()

    # Conecta el socket con la direccion.
    server.bind(("localhost", 6969))

    # Empieza a escuchar conexiones.
    server.listen(1)

    # Aceptamos una conexion, se bloquea hasta que alguien se conecte.
    print "Esperando conexion..."
    socket_cliente, datos_cliente = server.accept()
    # Imprime la información del cliente conectado.
    print "Conectado con: " + datos_cliente[0] + ":" + str(datos_cliente[1])

    while 1:
        print "Esperando mensaje..."
        # Esperamos que el cliente mande un mensaje y lo imprimimos.
        datos = socket_cliente.recv(1000)
        print "El mensaje es:", datos
        # Si el mensaje es "quit" se termina el bucle.
        if datos == "quit":
            #socket_cliente.send("chau")  
            break 

    print "Cerrando..."
    # Cerramos ambos sockets.
    socket_cliente.close()
    server.close()

if __name__ == "__main__":
    main()
