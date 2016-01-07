import pygame
import random
import sys
from pygame.locals import *
from field import *
from defines import *
from key import *

class Game:
  def __init__(self, screen):
    self.screen = screen
    self.clock = pygame.time.Clock()
    # default: standard
    self.field = Field(10, 20)
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

class Game1P(Game):
  def __init__(self, screen):
    Game.__init__(self, screen)
    self.counter = 0
    
  def start(self):
    while True:
      # restart
      self.field.restart()
      while True:
        # auto send line
        if self.counter % 400 == 0:
          self.field.recieveAttack(random.randint(1, 4))
        self.counter += 1
        # display
        self.screen.fill(BLACK)
        self.screen.blit(self.field.draw(), (20, 20))
        pygame.display.flip()
        # routine work
        quit, restart = Game.routine(self)
        if quit: return
        if restart: break


class Game1PInvisible(Game):
  def __init__(self, screen):
    Game.__init__(self, screen)
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

class Game1P4W(Game):
  def __init__(self, screen):
    Game.__init__(self, screen)
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
