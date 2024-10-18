from libs import socket, time
import sound
import movement
from sensors import color

HOST = ''
PORT = 65432

def start():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        
        print("Esperando conexoes porta: {}".format(PORT))
        
        conn, addr = s.accept()
        
        with conn:
            
            print("Conexao estabelecida a ".format(addr))
            
            while True:
                
                data = conn.recv(1024)
                if not data:
                    break
                
                msg = data.decode('utf-8')
                
                if msg == 'start':
                    while True:
                        movement.move_forward()
                        if color.getColor() == 'black':
                            movement.stop()
                            time.sleep(0.5)
                            movement.move_left()
                        elif color.getColor() == 'orange':
                            movement.stop()
                            sound.siren()  
                            # time.sleep(10)
                            break
                else:
                    print("Err -> mensagem desconhecida recebida: {}".format(msg))
                   
                   
def go_the_fire():
    while True:
        
        movement.move_forward()
        if color.getColor() == 'black':
            movement.stop()
            time.sleep(0.5)
            