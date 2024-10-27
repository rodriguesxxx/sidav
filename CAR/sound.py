from libs import Sound, time
import os
import subprocess

__sound = Sound()

__sound.set_volume(100)

def play_file(file, seconds = 0):
    process = subprocess.Popen(['/usr/bin/aplay', '-q', file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if seconds > 0:
        time.sleep(seconds)
        stop_file(process)
    return process

def stop_file(process):
    os.system('kill -2 {}'.format(process.pid))

    
def hello():
    __sound.speak("Hello")
    
def siren(): 
    play_file('/home/robot/assets/sirene.wav', 30)
        