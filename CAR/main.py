import sound
import movement
from sensors import color

def main():
    
    while True:
        movement.move_forward()
        if(color.getColor == 'black'):
            movement.move_left()
        
        #TODO: Verificar se chegou na cor do incendio e acionar sirene
            
if __name__ == "__main__":
    main()