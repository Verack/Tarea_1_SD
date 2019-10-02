import socket
import struct
import sys
import time
from random import randint
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from threading import Lock

file_cliente = open("registro_server.txt","w")
#file_server = #
##################VARIABLES GENERALES

ip = ''
puerto = 5000
lock=Lock()

##################FUNCIONES
def envio_msg(clientsocket, direc, sock):
    global msgq
    global datanodes

    msgq=[]
    datanodes=[]
    while True:

        data = clientsocket.recv(4096)
        IP = str(direc[0] + " - ").encode('utf-8')
        lock.acquire()
        if not data:
            fail = str("No Recibido").encode('utf-8')

            clientsocket.send(IP + fail)
            print("no")

        else:

            file_cliente.write(direc[0] + " - " + data.decode('utf-8'))
            file_cliente.write("\n")
            file_cliente.flush()

            lista = list(lista_datanodes_disponibles)

            ind = randint(0,len(lista)-1)

            datanodes.append(lista[ind])
            print(data)
            msgq.append(data)
            file_cliente.write("el mensaje del cliente "+direc[0]+" fue enviado al nodo "+str(lista[ind]))
            print(direc[0], (lista[ind]))
            file_cliente.flush()


            succ = str("Recibido"+str(lista[ind])).encode('utf-8')
            clientsocket.send(IP + succ)

        print("din")
        lock.release()

def multicaster(multicast_group, sock):
    global lista_datanodes_disponibles

    lista_datanodes_disponibles = set()
    message = ''
    # Send data to the multicast group


    # Look for responses from all recipients
    while True:
        lock.acquire()
        print ('sending "%s"' % message)
        sent = sock.sendto(str.encode(message), multicast_group)
        print ('waiting to receive')
        file = open("hearbeat_server.txt","a")
        try:
            data, server = sock.recvfrom(16)
        except socket.timeout:
            print ('timed out, no more responses')
            file.write("no response \n")
            file.flush()
        else:
            print ('received "%s" from %s' % (data, server))

            lista_datanodes_disponibles.add(server)
            file.write("conected "+str(server)+" \n")
            file.flush()
        if len(msgq)>0:
            print("passs")
            print(datanodes[0])
            sock.sendto(msgq[0],datanodes[0])
            data, server = sock.recvfrom(16)
            msgq.remove(msgq[0])
            datanodes.remove(datanodes[0])

        file.close
        lock.release()
        time.sleep(5)



##################MULTICAST

multicast_group = ('224.3.29.71', 10000)

# Create the datagram socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set a timeout so the socket does not block indefinitely when trying
# to receive data.
sock.settimeout(0.2)

# Set the time-to-live for messages to 1 so they do not go past the
# local network segment.
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)


############################

conexiones = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind((ip,puerto))
s.listen()

#################Cliente-Servidor


with ThreadPoolExecutor() as executor:
    while True:


        #Se acepta la conexion entrante
        clientsocket, direc = s.accept()

        print("Conneccion con {direc} ha sido establecida")

        #Se envia el mensaje
        clientsocket.send(bytes("Se ha conectado al servidor con el ip: "+str(ip)+" y puerto: "+str(puerto),"utf-8"))

        conexiones.append(clientsocket)

        executor.submit(envio_msg, clientsocket, direc,sock,)
        executor.submit(multicaster, multicast_group, sock,)
