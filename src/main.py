import threading
import socket

import constants as C
import roteador as R

class Main():
    
    def __init__(self):
        self.router = R.Roteador()
    
    def inicializar(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((C.HOST, C.PORT))
            sock.listen()
            while True:
                conn, endereco = sock.accept()
                thread = threading.Thread(target=self.router.handle_connection, args=(conn, endereco))
                thread.start()
                            
if __name__ == '__main__':
    main = Main()
    main.inicializar()