#TODO: receber o frame da ESP32
#TODO: aplicar a mascara sobre ele

from libs import *
from utils2 import parse_arguments
from colors import RED_LOWER, RED_UPPER, BLACK

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True) # carrega o modelo de detecção do YOLO

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

def _detection_people(frame): # usa o YOLO para detecção de pessoas
    results = model(frame)
    pred = results.pandas().xyxy[0]

    for index, row in pred.iterrows():
        box = [int(x) for x in row[['xmin', 'ymin', 'xmax', 'ymax']]] #retorna o "x" inicial, o "y" inicial, o "x" final e o "y" final para a demarcação da caixa delimitadora 
        confidence = round(row['confidence'] * 100, 0) # retorna a taxa de confiança da deteção em porcentagem
        class_id = int(row['class'])

        if class_id == 0: # checa se o id da classe é a mesma da classe "person"
            cv.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 0, 255), 2)
            cv.putText(frame, f'Pessoa {confidence}%', (box[0], box[1] - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
        return __process_frame(frame)
   
def init() -> None:
    args = parse_arguments(ArgumentParser())
    cam = __initialize_camera(args)

    try:
        while True:
            grabbed, frame = cam.read()
            
            if args.get("video") and not grabbed:
                break

            _detection_people(frame=frame)
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