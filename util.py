import pygame
from defines import *

# returns a colored block surface
def make_surface(color, size = BLOCK_SIZE):
  surface = pygame.Surface(size)
  surface.fill(color)
  return surface

# returns the center of all positions
def find_center(posList):
  xs = [float(x) for x, y in posList]
  ys = [float(y) for x, y in posList]
  return ((max(xs)+min(xs))/2, (max(ys)+min(ys))/2)
