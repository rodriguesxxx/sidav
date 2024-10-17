from libs import INPUT_1, ColorSensor

S1 = ColorSensor(INPUT_1)

__cores = {
    0: 'undefined',
    1: 'black'
}

def getColor():
    detected_color = S1.color
    color = __cores.get(detected_color, __cores['0'])
    return color