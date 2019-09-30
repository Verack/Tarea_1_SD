from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from concurrent.futures import ThreadPoolExecutor

class Server:
	def __init__(self, ip, puerto, name):
		self.s = self._start_sock(ip,puerto)
		self.file = open(name,"w")
		self.conexiones = []


	def run(self,ip,puerto):
		print("El Server esta activo")

		with ThreadPoolExecutor() as executor:
			while True:

				#Se acepta la conexion entrante
				clientsocket, direc = self.s.accept()

				print(f"Conneccion con {direc} ha sido establecida")

				#Se envia el mensaje
				clientsocket.send(bytes("Se ha conectado al servidor con el ip: "+str(ip)+" y puerto: "+str(puerto),"utf-8"))

				self.conexiones.append(clientsocket)

				executor.submit(self.envio_msg, clientsocket, direc)


	def envio_msg(self, clientsocket, direc):
		while True:
			data = clientsocket.recv(4096)

			IP = str(direc[0] + " - ").encode('utf-8')

			if not data:
				fail = str("No Recibido").encode('utf-8')

				clientsocket.send(IP + fail)

			else:
				self.file.write(direc[0] + " - " + data.decode('utf-8'))
				self.file.write("\n")
				self.file.flush()
				succ = str("Recibido").encode('utf-8')
				clientsocket.send(IP + succ)




	@staticmethod
	def _start_sock(ip,puerto):
		s = socket(AF_INET, SOCK_STREAM)
		s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
		s.bind((ip,puerto))
		s.listen()
		return s

if __name__ == '__main__':
	server = Server('0.0.0.0',5000,"./log.txt")
	server.run('0.0.0.0',5000)