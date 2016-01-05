import pygame
from field import *
from control import check_event

def main():
  pygame.init()
  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  field = Field(10, 20, 150, 20)

  while True:
    check_event(field)
    screen.fill(BLACK)
    field.draw(screen)
    pygame.display.flip()
    clock.tick(120)

if __name__ == "__main__":
  main()
