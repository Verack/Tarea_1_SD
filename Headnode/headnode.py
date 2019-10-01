import socket
import struct
import sys
import time

message = 'very important data'
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


try:

    # Send data to the multicast group


    # Look for responses from all recipients
    while True:
        print ('sending "%s"' % message)
        sent = sock.sendto(str.encode(message), multicast_group)
        print ('waiting to receive')
        file = open("t.txt","a")
        try:
            data, server = sock.recvfrom(16)
        except socket.timeout:
            print ('timed out, no more responses')
            file.write("no response \n")
        else:
            print ('received "%s" from %s' % (data, server))
            file.write("conected \n")
        file.close
        time.sleep(5)

finally:
    print ('closing socket')
    sock.close()
