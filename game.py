import pygame
import random
from field import *
from defines import *
from control import check_event

class Game:
  def __init__(self, screen):
    self.screen = screen
    self.clock = pygame.time.Clock()
    # default: standard
    self.field = Field(10, 20)

  def routine(self):
    self.clock.tick(120)
    return check_event(self.field)


class Game1P(Game):
  def __init__(self, screen):
    Game.__init__(self, screen)
    self.counter = 0
    
  def start(self):
    while True:
      # restart
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
