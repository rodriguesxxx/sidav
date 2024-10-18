from libs import INPUT_1, ColorSensor

S1 = ColorSensor(INPUT_1)

__cores = {
    0: 'unknown',
    1: 'black',
    5: 'orange'
}

def getColor():
    detected_color = S1.color
    color = __cores.get(detected_color, 'unknown')
    return color