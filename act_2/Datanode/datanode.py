import socket
import struct
import sys

multicast_group = '224.3.29.71'
server_address = ('', 10000)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind(server_address)


group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

while True:
    print ('\nEsperando recibir mensajes')
    data, address = sock.recvfrom(1024)

    print ('Recibido el mensaje %s desde %s' % (data, address))
    if len(data)>0:
        file=open("data"+ str(address[0])+".txt","a")
        file.write(str(data)+" \n")
        file.close


    print ('Mandando respuesta al Heartnode', address)
    sock.sendto(str.encode('Recibido'), address)
