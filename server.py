import socket
import threading

all_sockets = []
all_addr = []
clientnames = []
clientports = []


class Server(threading.Thread):
    def __init__(self):
        global all_sockets

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('0.0.0.0', 55558))
        self.sock.listen()

        print("Servidor aberto na porta 55558")

    def run(self):
        while(True):
            conn, addr = self.sock.accept()
            self.conn = conn
            print(f"Conectado com o cliente {addr}")
            
            clientports.append(addr)
            all_addr.append(addr)
            all_sockets.append(conn)

            name = self.conn.recv(1024).decode('utf-8')
            if not name:
                break
            clientnames.append(name)
            print(f"Temos agora {len(all_sockets)} conexões.")

            if (len(all_sockets)) == 2:
                for conn in all_sockets:
                    if all_sockets.index(conn) == 0:
                        conn.sendall(bytes((f"Conecte com: User: {clientnames[1]} IP: {clientports[1][0]}, Porta: {clientports[1][1]}"), 'utf-8'))
                    else:
                        conn.sendall(bytes((f"Conecte com: User: {clientnames[0]} IP: {clientports[1][0]}, Porta: {clientports[1][1]}"), 'utf-8'))
                    print("Mensagem enviada aos clientes")

if __name__=='__main__':
    srv = Server()
    thread1 = threading.Thread(target= srv.run)
    thread1.start()