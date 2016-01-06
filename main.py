import pygame
import random
from field import *
from control import check_event

def main():
  pygame.init()
  pygame.display.set_caption("PyTetris")
  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  field = Field(10, 20)

  cnt = 0

  while True:
    if cnt % 400 == 0:
      field.recieveAttack(random.randint(1, 4))
    cnt += 1

    check_event(field)
    screen.fill(BLACK)
    screen.blit(field.draw(), (20, 20))
    pygame.display.flip()
    clock.tick(120)

if __name__ == "__main__":
  main()
