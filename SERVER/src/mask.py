from libs import *
from utils import parse_arguments
from colors import RED_LOWER, RED_UPPER, BLACK


def __initialize_camera(args):
    if not args.get("video", False):
        return cv.VideoCapture(0)  # webcam
    else:
        return cv.VideoCapture(args["video"])

def __process_frame(frame):

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
   
def init() -> None:
    args = parse_arguments(ArgumentParser())
    
    cam = __initialize_camera(args)

    try:
        while True:
            
            grabbed, frame = cam.read()
            
            if args.get("video") and not grabbed:
                break

            frame = __process_frame(frame)
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