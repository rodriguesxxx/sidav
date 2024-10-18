import os

EV3_IP = '192.168.0.100'
EV3_PATH = './'
PC_PATH = '/home/the-pc/Projects/IFNMG/ignis/CAR'
TAR_FILE = '/tmp/car_files.tar'

# cmd = f'scp -r {PC_PATH} robot@{EV3_IP}:{EV3_PATH}'

cmd_create_tar = f'cd {PC_PATH} && tar -cvf {TAR_FILE} .'
os.system(cmd_create_tar)

cmd_scp = f'scp {TAR_FILE} robot@{EV3_IP}:{EV3_PATH}'
os.system(cmd_scp)

cmd_extract_tar = f'ssh robot@{EV3_IP} "cd {EV3_PATH} && tar -xvf {TAR_FILE} && rm {TAR_FILE}"'
os.system(cmd_extract_tar)

os.remove(TAR_FILE)