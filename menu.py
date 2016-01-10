import pygame
import sys
from pygame.locals import *
from defines import *

class Menu:
  def __init__(self, isRoot = False):
    self.options = []
    self.actions = []
    self.pointer = 0
    self.isRoot = isRoot
    self.clock = pygame.time.Clock()

  def start(self):
    assert len(self.options) > 0, "menu is empty!"
    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
          # next option
          if event.key == K_DOWN: 
            self.pointer += 1
            self.pointer %= len(self.options)
          # previous option
          elif event.key == K_UP: 
            self.pointer -= 1
            self.pointer %= len(self.options)
          # select option
          elif event.key == K_RETURN:
            self.actions[self.pointer]()
          # return to previous menu
          elif event.key == K_LEFT: 
            if not self.isRoot: return
      
      self.draw()
      pygame.display.flip()
      self.clock.tick(120)

  # add an option and corresponding action
  # if the option is selected, do the action
  def addOption(self, option, action):
    self.options.append(option)
    self.actions.append(action)

  def draw(self):
    surface = pygame.display.get_surface()
    f = pygame.font.SysFont("Consolas", 24)
    sum_height = 0
    # fill black background
    surface.fill(BLACK)
    # blit options
    for i in range(len(self.options)):
      color = YELLOW if i == self.pointer else WHITE
      text = f.render(self.options[i], 1, color)
      surface.blit(text, (0, sum_height))
      sum_height += text.get_height()
