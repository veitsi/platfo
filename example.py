import sys
import time

from arduino import Arduino
from multiprocessing import freeze_support


if __name__ == '__main__':
    freeze_support()
    device = Arduino()
    time.sleep(0.5)
    start = time.time()
    device.forwardMotor()
    while True:
        ###################################
        #
        if time.time() - start > 3:
            device.stopMotor()
            break
        ###################################
        time.sleep(0.05)
