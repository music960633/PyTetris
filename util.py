import pygame
from defines import *

# returns a colored block surface
def make_surface(color, size = BLOCK_SIZE):
  surface = pygame.Surface(size)
  surface.fill(color)
  return surface

# add a frame
def add_frame(surface, color, width):
  w, h = surface.get_size()
  frame = pygame.Surface((w + 2*width, h + 2*width))
  frame.blit(surface, (width, width))
  pygame.draw.rect(frame, color, frame.get_rect(), width)
  return frame

# returns the center of all positions
def find_center(posList):
  xs = [float(x) for x, y in posList]
  ys = [float(y) for x, y in posList]
  return ((max(xs)+min(xs))/2, (max(ys)+min(ys))/2)
