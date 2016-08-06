import sys
import time

from arduino import Arduino
from multiprocessing import freeze_support

distances = [[2,3],[4,5], [7,8], [10,11], [14,16]]
stopstart=0
delta=0
device=None

def start():
    global stopstart,delta, device
    delta+=time.time()-stopstart
    device.forwardMotor()


def stop():
    global stopstart,device
    stopstart=time.time()
    device.stopMotor()


def distance():
    global delta
    return time.time()-delta

def is_blocked():
    dist=distance()
    for i in distances:
        if i[0]>=dist>=i[1]:
            return True
    return False

delta=time.time()
device = Arduino()
stop()
start()
print distance()
time.sleep(0.5)
print distance()

if __name__ == '__main__':
    freeze_support()
    time.sleep(0.5)
    start = time.time()
    while True:
        ###################################
        #
        stopped=False
        if is_blocked() and not stopped:
            stop()
        elif stopped:
            start()

        # if time.time() - start > 3:
        #     device.stopMotor()
        #     break
        ###################################
        time.sleep(0.05)