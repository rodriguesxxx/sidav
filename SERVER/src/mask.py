from libs import *
from utils import parse_arguments
from definitions import RED_LOWER, RED_UPPER

def main() -> None:
    args = parse_arguments(ArgumentParser())
    
    if not args.get("video", False):
        cam = cv.VideoCapture(0) #webcam
    else:
        cam = cv.VideoCapture(args["video"])
    
    # TODO: capturar vídeo(por enquanto do propio PC)
    # TODO: construir máscara para a cor
    while(True):
        pass
    
    cam.release()
    cv.destroyAllWindows()
    
if __name__ == "__main__":
    main()