import socket
import threading

all_sockets = []
all_addr = []
clientnames = []
clientips = []
clientports = []


class Server(threading.Thread):
    def init(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('127.0.0.1', 55555))
        self.sock.listen()

        all_sockets.append(self.sock)
        print("Servidor aberto na porta 55555")

    def run(self):
        while(True):
            for sock in all_sockets:
                if sock == self.sock:
                    conn, addr = self.sock.accept()
                    print(f"Conectado com o cliente {addr}")
                    all_addr.append(addr)
                    all_sockets.append(conn)
                    print(f"Temos agora {len(all_sockets) - 1} conexões.")
                else: 
                    try:
                        s = sock.recv(1024)
                        chunks = s.split(' ')
                        clientnames.append(chunks[1])
                        clientips.append(chunks[3])
                        clientports.append(chunks[5])
                    except:
                        print(f"Erro ao conectar com {str(sock.getpeername())}")


class Connections(threading.Thread):
    def run(self):
        for conn in all_sockets[1:]:
            conn_number = all_sockets.index(conn)
            if conn_number == 1:
                conn.sendall(f"Conecte-se com: \nUser: {clientnames[2]} \nIP: {clientips[2]} \nPorta: {clientports[2]}")
                print("Mensagem enviada ao 1o cliente")
            else:
                conn.sendall(f"Conecte-se com: \nUser: {clientnames[1]}\nIP: {clientips[1]}\nPorta: {clientports[1]}")
                print("Mensagem enviada ao 2o cliente")
        print("acabei")
        conn.close()

if __name__=='__main__':
    srv = Server()
    srv.init()
    srv.start()
    print(all_sockets)
    ctrl = Connections()
    ctrl.start()