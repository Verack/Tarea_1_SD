from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from time import sleep

class Client:
	def __init__(self,ip,puerto,name):
		self.s = self._start_sock(ip,puerto)
		self.file = open(name,"w")

		thread = Thread(target=self.send_message)
		thread.daemon = True
		thread.start()

		while True:

			data = self.s.recv(4096)
			if not data:
				self.file.close()
				break
			print(data.decode("utf-8"))
			self.file.write(data.decode("utf-8"))
			self.file.write("\n")
			self.file.flush()

	def send_message(self):
		while True:
			sleep(5)
			user_message = "Mensaje del cliente :D"
			self.s.send(user_message.encode("utf-8"))


	@staticmethod
	def _start_sock(ip,puerto):
		s = socket(AF_INET, SOCK_STREAM)
		s.connect((ip,puerto))
		return s

if __name__ == '__main__':
	cliente = Client('headnode',5000,"./registro_cliente.txt")
