import socket
import struct
import sys
import time
from random import randint
from concurrent.futures import ThreadPoolExecutor


file_cliente = open("registro_server.txt","w")
#file_server = #
time.sleep(5)

##################VARIABLES GENERALES

ip = ''
puerto = 5000


##################FUNCIONES
def envio_msg(clientsocket, direc, sock):
    while True:
        data = clientsocket.recv(4096)

        IP = str(direc[0] + " - ").encode('utf-8')

        if not data:
            fail = str("No Recibido").encode('utf-8')

            clientsocket.send(IP + fail)

        else:
            file_cliente.write(direc[0] + " - " + data.decode('utf-8'))
            file_cliente.write("\n")
            file_cliente.flush()

            lista = list(lista_datanodes_disponibles)
            ind = randint(0,len(lista))
            sock.send(data, lista[ind])
            file_cliente.write("el mensaje del cliente "+direc[0]+" fue enviado al nodo "+str(lista[ind]))
            file_cliente.flush()

            succ = str("Recibido").encode('utf-8')
            clientsocket.send(IP + succ)

def multicaster(multicast_group, sock):
    global lista_datanodes_disponibles
    lista_datanodes_disponibles = set()
    message = 'very important data'
    # Send data to the multicast group


    # Look for responses from all recipients
    while True:
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
        file.close
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

        print(f"Conneccion con {direc} ha sido establecida")

        #Se envia el mensaje
        clientsocket.send(bytes("Se ha conectado al servidor con el ip: "+str(ip)+" y puerto: "+str(puerto),"utf-8"))

        conexiones.append(clientsocket)

        executor.submit(envio_msg, clientsocket, direc)
        executor.submit(multicaster, multicast_group, sock)





