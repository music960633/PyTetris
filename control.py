import sys
import pygame
from pygame.locals import *

# keypress counter
count = {
    K_LEFT  : 0,
    K_RIGHT : 0,
    K_DOWN  : 0,
    K_UP    : 0,
    K_x     : 0,
    K_z     : 0,
    K_SPACE : 0,
    K_c     : 0,
    K_F2    : 0,
}

# counter threshold, used as DAS (delay auto shift)
threshold = {
    K_LEFT  : 17,
    K_RIGHT : 17,
    K_DOWN  : 0,
    K_UP    : 1e10,
    K_x     : 1e10,
    K_z     : 1e10,
    K_SPACE : 1e10,
    K_c     : 1e10,
    K_F2    : 1e10
}

# call functions corresponding to the key
def execute(field, key):
  if key == K_LEFT:
    field.moveMino((-1, 0))
  elif key == K_RIGHT:
    field.moveMino((1, 0))
  elif key == K_DOWN:
    field.moveMino((0, -1))
  elif key == K_UP:
    field.turnMino(False)
  elif key == K_x:
    field.turnMino(False)
  elif key == K_z:
    field.turnMino(True)
  elif key == K_SPACE:
    field.dropMino()
  elif key == K_c:
    field.holdMino()
  elif key == K_F2:
    field.restart()

# check events
def check_event(field):
  for event in pygame.event.get():
    if event.type == pygame.QUIT: sys.exit()
    elif event.type == pygame.KEYDOWN:
      if event.key in count:
        count[event.key] += 1
        if count[event.key] == 1 or count[event.key] > threshold[event.key]:
          execute(field, event.key)
    elif event.type == pygame.KEYUP:
      if event.key in count:
        count[event.key] = 0

  pressed = pygame.key.get_pressed()
  for key in count:
    if pressed[key] == 1:
      count[key] += 1
      if count[key] == 1 or count[key] > threshold[key]:
        execute(field, key)
    else:
      count[key] = 0
