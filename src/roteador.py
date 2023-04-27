import time
import constants as C

class Roteador:
    def __init__(self):
        self.tabela_roteamento = {}
        self.ip_roteador = C.IP_ROTEADOR                  
                     
    def atualizar_tabela_roteamento(self, ip_destino, interface_rede, metrica, conexao):
        if ip_destino not in self.tabela_roteamento:
            self.tabela_roteamento[ip_destino] = {'interface_rede': interface_rede, 'salto':self.ip_roteador, 'metrica': metrica + 1, 'conexao': conexao, 'endereco':ip_destino}                                                                   
        else:
            if ip_destino == self.tabela_roteamento[ip_destino]['endereco'] and self.tabela_roteamento[ip_destino]['metrica'] + 1 < metrica:
                self.tabela_roteamento[ip_destino] = {'interface_rede': interface_rede, 'salto':self.ip_roteador, 'metrica': metrica + 1, 'conexao': conexao}  
                
            elif self.tabela_roteamento[ip_destino]['metrica'] + 1 < metrica:
                self.tabela_roteamento[ip_destino] = {'interface_rede': interface_rede, 'salto':self.ip_roteador, 'metrica': metrica + 1, 'conexao': conexao, 'endereco':ip_destino}                             
                        
    def enviar_pacote(self, ip_origem, ip_destino, ttl, tos):
        # Valida se o IP de origem está na tabela de roteamento
        if ip_destino not in self.tabela_roteamento:
            return f"{ip_origem} não encontrado na tabela."
        else:
            interface_rede = self.tabela_roteamento[ip_destino]['interface_rede']
            print("def enviar_pacote")
            return f"Enviando pacote de {ip_origem} para {ip_destino}"
          

    def handle_connection(self, conn, endereco):        
        while True:            
            dados = conn.recv(1024)
            if not dados:
                break
            response = ''
            chave, dados = dados.decode().split(':')            
            if chave == "0":
                destino, interface_rede, metrica = dados.split(',')
                self.atualizar_tabela_roteamento(destino, interface_rede, int(metrica), conn)
            elif chave == "1":                
                origem, destino, ttl, tos = dados.split(',')
                response = self.enviar_pacote(origem, destino, int(ttl), int(tos))
                value = self.tabela_roteamento.get(destino)
                if value is not None:
                    conexao = value['conexao']
                    conexao.sendall(response.encode())        
        