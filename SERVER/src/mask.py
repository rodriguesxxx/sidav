#TODO: receber o frame da ESP32
#TODO: aplicar a mascara sobre ele

from libs import *
from utils2 import parse_arguments
from colors import RED_LOWER, RED_UPPER, BLACK

id_classes = [0,14,15,16,17,18,19,20,21,22,23] # IDs das classes a serem identificadas 

model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True) # carrega o modelo de detecção do YOLO
model.classes = id_classes # apenas essas classes serão detectadas

class_names = { # dicionário com os nomes traduzidos das classes a serem identificadas  
  0:  'Pessoa',
  14: 'Passaro',
  15: 'Gato',
  16: 'Cachorro',
  17: 'Cavalo',
  18: 'Ovelha',
  19: 'Vaca',
  20: 'Elefante',
  21: 'Urso',
  22: 'Zebra',
  23: 'Girafa'
}

def __initialize_camera(args): # inicializa a camera
    if not args.get("video", False):
        return cv.VideoCapture(0)  # webcam
    else:
        return cv.VideoCapture(args["video"])

def __process_frame(frame): # processa, formata e retorna o frame com a detecção do objeto por cor  
    frame = imutils.resize(frame, width=720)
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    mask = cv.inRange(hsv, RED_LOWER, RED_UPPER)
    mask = cv.erode(mask, None, iterations=2)
    mask = cv.dilate(mask, None, iterations=2)

    red_contours = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[-2]
    red_center_id = None

    if len(red_contours) > 0:
        contour_area = max(red_contours, key=cv.contourArea)
        rectangle = cv.minAreaRect(contour_area)
        box = cv.boxPoints(rectangle)
        box = np.int32(box)
        moments = cv.moments(contour_area)
        red_center_id = (int(moments["m10"] / moments["m00"]), int(moments["m01"] / moments["m00"]))
        cv.drawContours(frame, [box], 0, BLACK, 2)

    return frame

def _general_detection(frame): # usa o YOLO para detecção de pessoas e animais
    results = model(frame)

    pred = results.pandas().xyxy[0]

    for index, row in pred.iterrows():
        box = [int(x) for x in row[['xmin', 'ymin', 'xmax', 'ymax']]] #retorna o "x" inicial, o "y" inicial, o "x" final e o "y" final para a demarcação da caixa delimitadora 
        confidence = round(row['confidence'] * 100, 0) # retorna a taxa de confiança da deteção em porcentagem
        id_identified = int(row['class'])
        
        if id_classes != 0:
            for i in id_classes:
                if i == id_identified: # verifica se o ID identificado corresponde a algum dos IDs passados por parametro no array "list_id_classes"
                    class_name = class_names[i] # caso seja, recupera o nome da classe pelo ID no dicionário "class_names"
                    cv.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (255, 0, 0), 2)
                    cv.putText(frame, f'{class_name} {confidence}%', (box[0], box[1] - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        else:
            print("Lista de IDs vazia!")

        return __process_frame(frame)    

def init() -> None:
    args = parse_arguments(ArgumentParser())
    cam = __initialize_camera(args)

    try:
        while True:
            grabbed, frame = cam.read()
            
            if args.get("video") and not grabbed:
                break

            _general_detection(frame=frame)
            cv.imshow("Frame", frame)
            
            if cv.waitKey(1) & 0xFF == ord('s'):
                break

    except Exception as e:
        print(f"Erro inesperado: {e}")
    finally:
        cam.release()
        cv.destroyAllWindows()
    
if __name__ == "__main__":
    init()