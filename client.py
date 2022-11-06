import socket
import threading
from datetime import date, datetime

now = datetime.now

class Client(threading.Thread):
    message_count = 0
    name = ""
    peer_name = ""
    peer_ip = ""
    peer_port = ""

    def __init__(self, name):
        self.name = name
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Iniciando conexão com servidor...")
        self.sock.connect(('127.0.0.1', 55555))
        print("Conectado com servidor na porta 55555.")
        self.sock.sendall("Tô ligado!")
        self.sock.sendall(f"User: {name} \nIP: {self.sock.gethostbyname(self.socket.gethostname())} - porta: 55555")

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.peer_ip, self.peer_port))
        print(f"Conectado com o outro cliente {self.peer_name}")
    
    def receive_from_server(self):
        while True:
            data = self.sock.recv(1024).decode('ascii')
            if not data:
                break
        chunks = data.split(' ')
        self.peer_name = chunks[3]
        self.peer_ip = chunks[5]
        self.peer_port = chunks[7]
        self.sock.close()

    
    def send_to_client(self):
        msg = input("Insira sua mensagem: ")
        self.message_count += 1
        to_send = self.sock.send(f"{self.name} ({datetime.now}) #{self.message_count}:  {msg}\n")
        self.sock.sendall(to_send)

    def receive_from_client(self):
        while True:
            rcvd = self.client.recv(1024).decode('ascii')

            if rcvd == 'Confirmacao':
                print(f'{self.peer_name} diz #{self.message_count} recebida')
            else:
                date = datetime.now().strftime("%d/%m/%Y %H:%M")
                print(f'{self.name} #{self.message_count} (enviado {rcvd[0:16]}h/recebido {date}h):{rcvd[18:]}')
                self.client.send('Confirmacao'.encode('ascii'))

                messagesNumber += 1


    def end(self):
        self.message_count += 1
        self.client.sendall(f"Adeus, {self.peer_name}.\n")
        self.client.close()

if __name__=='__main__':
    name = input("Seu nome: ")
    cli1 = Client(name)
    thread1 = threading.Thread(target=cli1.receive_from_server)
    thread1.start()
    thread2 = threading.Thread(target=cli1.send_to_client)
    thread2.start()