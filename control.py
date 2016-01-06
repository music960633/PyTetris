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
    K_r     : 0,
    K_q     : 0
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
    K_r     : 1e10,
    K_q     : 1e10
}

# call functions corresponding to the key
# returns True if need to exit
def execute(field, key):
  quit, restart = False, False
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
  elif key == K_r:
    field.restart()
    restart = True
  elif key == K_q:
    quit = True
  return quit, restart

# check events, returns True if need to exit
def check_event(field):
  for event in pygame.event.get():
    if event.type == pygame.QUIT: sys.exit()
    '''
    elif event.type == pygame.KEYDOWN:
      if event.key in count:
        count[event.key] += 1
        if count[event.key] == 1 or count[event.key] > threshold[event.key]:
          if execute(field, event.key):
            return True
    elif event.type == pygame.KEYUP:
      if event.key in count:
        count[event.key] = 0
    '''
  quit, restart = False, False
  pressed = pygame.key.get_pressed()
  for key in count:
    if pressed[key] == 1:
      count[key] += 1
      if count[key] == 1 or count[key] > threshold[key]:
        q, r = execute(field, key)
        if q: quit = True
        if r: restart = True
    else:
      count[key] = 0
  return quit, restart
