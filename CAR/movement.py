from libs import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, time

M1 = LargeMotor(OUTPUT_A)
M2 = LargeMotor(OUTPUT_B)

# def move_forward(speed = 30):
    
#     M1.on(SpeedPercent(speed))
#     M2.on(SpeedPercent(speed))
def move_forward(speed = 30, seconds = 0):
    
    M1.on(SpeedPercent(speed), block=False)
    M2.on(SpeedPercent(speed+0.5), block=False)
    
    if seconds > 0:
        time.sleep(seconds)
        stop()
    
def move_backward(speed = 30, seconds = 0):
    
    M1.on(SpeedPercent(speed * (-1)), block=False)
    M2.on(SpeedPercent((speed + 0.5) * (-1)), block=False)
    
    if seconds > 0:
        time.sleep(seconds)
        stop()

def move_left(speed = 20):
    
    M1.on_for_seconds(SpeedPercent(speed * (-1)), 1.83, block=False)
    M2.on_for_seconds(SpeedPercent(speed), 1.83, block=True)

def move_left2(speed = 20):
    
    M1.on_for_seconds(SpeedPercent(speed * (-1)), 1.95, block=False)
    M2.on_for_seconds(SpeedPercent(speed), 1.95, block=True) 

def move_right(speed = 20):
    
    M1.on_for_seconds(SpeedPercent(speed), 1.83, block=False)
    M2.on_for_seconds(SpeedPercent(speed * (-1)) , 1.83, block=True)
    



def stop():
    
    M1.off()
    M2.off()
