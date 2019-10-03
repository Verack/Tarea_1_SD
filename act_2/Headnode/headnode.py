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
            msgq.append(data)
            file_cliente.write("El mensaje del cliente "+direc[0]+" fue enviado al nodo "+str(lista[ind])+" \n")

            file_cliente.flush()


            succ = str("Recibido"+str(lista[ind])).encode('utf-8')
            clientsocket.send(IP + succ)
        lock.release()

def multicaster(multicast_group, sock):
    global lista_datanodes_disponibles

    lista_datanodes_disponibles = set()
    message = ''


    #Envio de mensajes multicast
    while True:
        lock.acquire()
        print ('Enviando... "%s"' % message)
        sent = sock.sendto(str.encode(message), multicast_group)
        print ('En espera de respuesta')
        file = open("hearbeat_server.txt","a")
        try:
            data, server = sock.recvfrom(16)
        except socket.timeout:
            print ('Time out, no hubo respuesta del datanode')
            file.write("El datanode no responde \n")
            file.flush()
        else:
            print ('Respuesta "%s" del datanode %s' % (data, server))

            lista_datanodes_disponibles.add(server)
            file.write("Conexion con el datanode "+str(server)+" \n")
            file.flush()
        #En caso de que el cliente envie un mensaje, este se envia a un datanode.
        if len(msgq)>0:
            sock.sendto(msgq[0],datanodes[0])
            data, server = sock.recvfrom(16)
            print("Mensaje del cliente almacenado en el datanode "+str(datanodes[0]))
            msgq.remove(msgq[0])
            datanodes.remove(datanodes[0])

        file.close
        lock.release()
        time.sleep(5)



##################MULTICAST

multicast_group = ('224.3.29.71', 10000)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Time out de respuesta de los Datanodes
sock.settimeout(0.2)

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
