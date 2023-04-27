import socket
import time
import threading
import constants as C
import random

class Interface:
    def __init__(self, id, destino, nome, metrica):
        # Define os atributos recebidos como parâmetro
        self.id = id
        self.destino = destino
        self.nome = nome
        self.metrica = metrica               
        # Cria sockets TCP/IP
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Realiza conexão
        self.sock.connect((C.HOST, C.PORT))
        
    def enviar_pacote(self):
        data = f"0:{self.destino},{self.nome},{self.metrica}".encode()
        self.sock.sendall(data)            
        time.sleep(5)
        
    def receber_pacote(self):        
        response = self.sock.recv(1024)            
        time.sleep(5)                                

    def __del__(self):
        self.sock.close()


if __name__ == '__main__':
    # Lista com as 4 interfaces
    interfaces = [
        Interface(1 ,C.IP1, "eth0", C.METRICA),
        Interface(2, C.IP2, "eth1", C.METRICA),
        Interface(3, C.IP3, "eth2", C.METRICA),
        Interface(4, C.IP4, "eth3", C.METRICA)
    ]
        
    # Cria duas threads para cada interface de rede
    # Uma de envio e outra de recebimento
    threads_envio = []
    threads_receb = []
                
    for interf in interfaces:
        thread_envio = threading.Thread(target=interf.enviar_pacote)
        thread_envio.start()        
        threads_envio.append(thread_envio)    
        
    for interf in interfaces:    
        thread_receb = threading.Thread(target=interf.receber_pacote)
        thread_receb.start()
        threads_receb.append(thread_receb)             
    
    # Join das Threads de envio
    for thread_send in threads_envio:
        thread_send.join()

    # Join das Threads de receb
    for thread_receive in threads_receb:
        thread_receive.join()            
        