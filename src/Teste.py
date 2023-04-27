import socket
import constants as C

class Teste:
    if __name__ == '__main__':
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((C.HOST, C.PORT))     
            data = f"1:{C.IP1},{C.IP2},{ C.TTL},{5}".encode()            
            sock.sendall(data)
            response = sock.recv(1024)     
            sock.close()    