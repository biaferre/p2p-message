import socket
import threading
from datetime import datetime
from server import *

now = datetime.now

class Client_2(threading.Thread):
    message_count = 0
    name = ""
    peer_name = ""
    peer_ip = ""
    peer_port = ""

    def __init__(self, name):
        self.name = name
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Iniciando conexão com servidor...")
        self.sock.connect(('0.0.0.0', 55558))
        print("Conectado com servidor na porta 55558.")
        self.sock.sendall(bytes((f"{name}"), 'utf-8'))
    
    def receive_from_connections(self):
        data = self.sock.recv(1024).decode('utf-8')
        chunks = data.split(' ')
        self.peer_name = chunks[3]
        self.peer_ip = (chunks[5].removesuffix(","))
        self.peer_port = chunks[7]

        print(self.peer_ip.removesuffix(","))
        print(self.peer_port)

        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.close()

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('0.0.0.0', int(self.peer_port) + 5))
        print("Estabelecendo Conexao")

        thread2 = threading.Thread(target=self.send_to_client)

        thread2.start()

    
    def send_to_client(self):
        self.message_count += 1

        msg = input("Insira sua mensagem: ")
        date = datetime.now().strftime("%d/%m/%Y %H:%M")

        self.client.sendall(bytes((f"{self.name}: ({date}) #{self.message_count}:  {msg}\n"), 'utf-8'))

        thread3 = threading.Thread(target=self.receive_from_client)
        thread3.start()


    def receive_from_client(self):
        while True:
            rcvd = self.client.recv(1024).decode('utf-8')

            if rcvd == 'Confirmacao':
                print(f'{self.peer_name} diz #{self.message_count} recebida')
                thread3 = threading.Thread(target=self.receive_from_client)
                thread3.start()
            else:
                self.message_count += 1

                chunks = rcvd.split(" ")
                print(f'{self.name} #{self.message_count} (enviado {chunks[1].removeprefix("(")} {chunks[2]}{rcvd[27:]}')
                self.client.send('Confirmacao'.encode('utf-8'))

                thread2 = threading.Thread(target=self.send_to_client)

                thread2.start()



    def end(self):
        self.message_count += 1
        self.client.sendall(f"Adeus, {self.peer_name}.\n")
        self.client.close()


if __name__=='__main__':
    name = input("Seu nome: ")
    cli = Client_2(name)

    thread1 = threading.Thread(target=cli.receive_from_connections)
    thread1.start()
