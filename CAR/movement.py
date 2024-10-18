from libs import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent

M1 = LargeMotor(OUTPUT_A)
M2 = LargeMotor(OUTPUT_B)

def move_forward(speed = 30):
    
    M1.on(SpeedPercent(speed))
    M2.on(SpeedPercent(speed))

def move_left(speed = 20):
    
    M1.on_for_seconds(SpeedPercent(speed * (-1)), 1.65, block=False)
    M2.on_for_seconds(SpeedPercent(speed), 1.65, block=True)
    

def move_right(speed = 20):
    
    M1.on_for_seconds(SpeedPercent(speed), 1.65, block=False)
    M2.on_for_seconds(SpeedPercent(speed * (-1)) , 1.65, block=True)
    

def stop():
    
    M1.off()
    M2.off()