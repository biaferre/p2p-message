import socket
import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 55555))
server.listen()

clients = []
nicknames = []
addresses = []

def broadcast(message):
    for client in clients:
        client.send(message)

def receive():
    while True:
        client, address = server.accept()

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)
        addresses.append(address)

        print(f"{nickname} está online!")
        print(f"Informações do endereço: {str(address)}")

        if len(clients) == 2:
            for nick in nicknames:
                broadcast(nick.encode('ascii'))
                time.sleep(1)
            
            time.sleep(1)
            broadcast('new connection'.encode('ascii'))

receive()