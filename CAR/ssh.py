# ACESSAR SERVIDOR SSH
#ssh robot@192.168.0.100
#senha: maker

import os

EV3_IP = '192.168.0.101'
EV3_PATH = './'
PC_PATH = '/home/the-pc/Projects/IFNMG/ignis/CAR'
TAR_FILE = '/tmp/car_files.tar'

cmd = f'scp -r {PC_PATH} robot@{EV3_IP}:{EV3_PATH}'

os.system(cmd)