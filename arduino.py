import pygame
import sys

from multiprocessing import Process, Pipe

def device(pipe):
    pygame.init()
    surface = pygame.display.set_mode((500, 200))
    clock = pygame.time.Clock()

    frameColor = (255, 0, 0)
    hammerColor = (255, 255, 0)
    motorColor = (255, 255, 255)
    blackColor = (0, 0, 0)

    motor = 0
    motor_v = 0
    motor_speed = 320 / 5  # We want to move 320 pixels in 5 seconds.
    hammers = [0, 0, 0, 0, 0]

    receiving = False
    start = pygame.time.get_ticks()

    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          sys.exit()
      if receiving:
        if pipe.poll():
          receiving = False
          command = pipe.recv()
          if command == '1':
              motor_v = 0
          elif command == '2':
              motor_v = -motor_speed
          elif command == '3':
              motor_v = motor_speed
          elif command == '4':
              pipe.send(str(motor) + "\n")
          elif command == '5':
              for hammer in hammers:
                  pipe.send(str(hammer) + "\n")
          elif command == '99':
              sys.exit()
      else:
        pipe.send("w\n")
        receiving = True

      surface.fill(blackColor)
      pygame.draw.rect(surface, frameColor, pygame.Rect(10, 60, 480, 80), 1)
      pygame.draw.rect(surface, motorColor, pygame.Rect(20 + motor, 80, 40, 40))
      for i in range(len(hammers)):
          if hammers[i] == 0:
              pygame.draw.rect(surface, hammerColor, pygame.Rect(81 + i*76, 30, 10, 40))
          else:
              pygame.draw.rect(surface, hammerColor, pygame.Rect(81 + i*76, 80, 10, 40))
      pygame.display.flip()

      clock.tick(60)

      motor += motor_v * clock.get_time() / 1000
      # Time since the beginning in seconds.
      steps = (pygame.time.get_ticks() - start) / 1000

      if steps % 5 == 1:
          hammers[0] = 1
      else:
          hammers[0] = 0

      if steps % 10 > 6:
          hammers[1] = 1
      else:
          hammers[1] = 0

      if steps % 7 == 3 or steps % 7 == 4:
          hammers[2] = 1
      else:
          hammers[2] = 0

      if steps % 3 == 2:
          hammers[3] = 1
      else:
          hammers[3] = 0

      if steps % 3 == 2:
          hammers[4] = 1
      else:
          hammers[4] = 0

class Arduino(object):

    def __init__(self):
        self.parent_pipe, child_pipe = Pipe()
        p = Process(target=device, args=(child_pipe,))
        p.start()

    def stopMotor(self):
        self.__sendData('1')

    def backwardMotor(self):
        self.__sendData('2')

    def forwardMotor(self):
        self.__sendData('3')

    def getMotor(self):
        self.__sendData('4')
        return self.__getData()

    def getHammer(self):
        self.__sendData('5')
        v1 = self.__getData()
        v2 = self.__getData()
        v3 = self.__getData()
        v4 = self.__getData()
        v5 = self.__getData()
        return (int(v1), int(v2), int(v3), int(v4), int(v5))

    def close(self):
        self.__sendData('99')

    def __sendData(self, serial_data):
        while self.__getData()[0] != "w":
            pass
        self.parent_pipe.send(serial_data)

    def __getData(self):
        data = self.parent_pipe.recv()
        return data
