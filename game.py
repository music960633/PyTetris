import pygame
import random
from field import *
from defines import *
from control import check_event

class Game:
  def __init__(self, screen, style):
    self.screen = screen
    self.clock = pygame.time.Clock()
    self.counter = 0
    if style == "1P":
      self.field = Field(10, 20)

  def start(self):
    while True:
      if self.counter % 400 == 0:
        self.field.recieveAttack(random.randint(1, 4))
      self.counter += 1

      check_event(self.field)
      self.screen.fill(BLACK)
      self.screen.blit(self.field.draw(), (20, 20))
      pygame.display.flip()
      self.clock.tick(120)
