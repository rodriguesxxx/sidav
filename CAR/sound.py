from libs import Sound, time

__sound = Sound()

__sound.set_volume(100)

def hello():
    __sound.speak("Hello")
    
def siren(): 
    __sound.play_file('/home/robot/CAR/assets/sirene.wav', volume=100)
        