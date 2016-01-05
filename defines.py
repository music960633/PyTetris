import pygame

'''   size parameters   '''
SCREEN_WIDTH  = 500
SCREEN_HEIGHT = 500
SCREEN_SIZE   = (SCREEN_WIDTH, SCREEN_HEIGHT)
BLOCK_WIDTH   = 20
BLOCK_SIZE    = (BLOCK_WIDTH, BLOCK_WIDTH)

'''   RGB colors   '''
BLACK   = (  0,   0,   0)
GRAY    = ( 30,  30,  30)
WHITE   = (255, 255, 255)
RED     = (255,   0,   0)
GREEN   = (  0, 255,   0)
BLUE    = (  0,   0, 255)
CYAN    = (  0, 255, 255)
YELLOW  = (255, 255,   0)
MAGENTA = (255,   0, 255)
ORANGE  = (255, 140,   0)
GHOST   = (100, 100, 100)

# returns a colored block surface
def make_surface(color):
  surface = pygame.Surface(BLOCK_SIZE)
  surface.fill(color)
  return surface
