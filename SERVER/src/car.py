from libs import socket

HOST = '192.168.0.100'  
PORT = 65432

def start():
    msg = 'start'
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))  
        s.sendall(msg.encode('utf-8'))  
        print(f"Mensagem '{msg}' enviada para o EV3")
