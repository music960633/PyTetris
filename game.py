import pygame
import random
import sys
from pygame.locals import *
from field import Field
from defines import *
from key import KeyHandler

class Game:
  def __init__(self, canhold, table, numpack, next_size):
    self.screen = pygame.display.get_surface()
    self.clock = pygame.time.Clock()
    # default: standard
    self.field = Field(10, 20, canhold=canhold, table=table, numpack=numpack, next_size=next_size)
    self.initKeyHandler()

  def initKeyHandler(self):
    self.keyHandler = KeyHandler()
    self.keyHandler.addKey(K_LEFT , True, 120, 12)
    self.keyHandler.addKey(K_RIGHT, True, 120, 12)
    self.keyHandler.addKey(K_DOWN , True, 12 , 12)
    self.keyHandler.addKey(K_UP   , False)
    self.keyHandler.addKey(K_x    , False)
    self.keyHandler.addKey(K_z    , False)
    self.keyHandler.addKey(K_SPACE, False)
    self.keyHandler.addKey(K_c    , False)
    self.keyHandler.addKey(K_r    , False)
    self.keyHandler.addKey(K_q    , False)

  def routine(self):
    # for exit
    for event in pygame.event.get():
      if event.type == pygame.QUIT: sys.exit()
    # key presses
    time = self.clock.tick(120)
    quit, restart = False, False
    for key in self.keyHandler.getTrigger(time):
      if key == K_LEFT    : self.field.moveMino((-1, 0))
      elif key == K_RIGHT : self.field.moveMino((1, 0))
      elif key == K_DOWN  : self.field.moveMino((0, -1))
      elif key == K_UP    : self.field.turnMino(False)
      elif key == K_x     : self.field.turnMino(False)
      elif key == K_z     : self.field.turnMino(True)
      elif key == K_SPACE : self.field.dropMino()
      elif key == K_c     : self.field.holdMino()
      elif key == K_r     : restart = True
      elif key == K_q     : quit = True
    return quit, restart

class Game1pNormal(Game):
  def __init__(self, canhold=True, table='SRS', numpack=1, next_size=5):
    Game.__init__(self, canhold, table, numpack, next_size)
    self.counter = 0
    
  def start(self):
    while True:
      # restart
      self.field.restart()
      while True:
        # display
        self.screen.fill(BLACK)
        self.screen.blit(self.field.draw(), (20, 20))
        pygame.display.flip()
        # routine work
        quit, restart = Game.routine(self)
        if quit: return
        if restart: break


class Game1pInvisible(Game):
  def __init__(self, canhold=True, table='SRS', numpack=1, next_size=5):
    Game.__init__(self, canhold, table, numpack, next_size)
    self.field = Field(10, 20, invisible = True)
    
  def start(self):
    while True:
      # restart
      self.field.restart()
      while True:
        # display
        self.screen.fill(BLACK)
        self.screen.blit(self.field.draw(), (20, 20))
        pygame.display.flip()
        # routine work
        quit, restart = Game.routine(self)
        if quit: return
        if restart: break

class Game1pDig(Game):
  def __init__(self, canhold=True, table='SRS', numpack=1, next_size=5):
    Game.__init__(self, canhold, table, numpack, next_size)
    
  def start(self):
    while True:
      # restart
      self.field.restart()
      self.counter = 0
      threshold = 300
      accumulate = 0
      while True:
        # auto send line
        self.counter += 1
        if self.counter > threshold and not self.field.gameover:
          self.field.recieveAttack(1)
          self.field.clearAttack()
          self.counter = 0
          accumulate += 1
        # display
        self.screen.fill(BLACK)
        self.screen.blit(self.field.draw(), (20, 20))
        pygame.display.flip()
        # routine work
        quit, restart = Game.routine(self)
        if quit: return
        if restart: break


class Game1p4wide(Game):
  def __init__(self, canhold=True, table='SRS', numpack=1, next_size=5):
    Game.__init__(self, canhold, table, numpack, next_size)
    self.field = Field(4, 20)

  def start(self):
    while True:
      # restart
      self.field.restart()
      self.field.recieveAttack(1)
      self.field.clearAttack()
      while True:
        # display
        self.screen.fill(BLACK)
        self.screen.blit(self.field.draw(), (20, 20))
        pygame.display.flip()
        # routine work
        quit, restart = Game.routine(self)
        if quit: return
        if restart: break
