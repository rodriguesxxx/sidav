import socket
import time
HOST = '192.168.0.100'  
PORT = 65432 
 
mensagem = 'start'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))  
    s.sendall(mensagem.encode('utf-8'))  
    print(f"Mensagem '{mensagem}' enviada para o EV3")
