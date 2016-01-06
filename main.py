import sys
import pygame
from pygame.locals import *
from game import *
from defines import *

def main():
  pygame.init()
  pygame.display.set_caption("PyTetris")
  screen = pygame.display.set_mode(SCREEN_SIZE)
  
  menu(screen)

def menu(screen):
  while True:
    f = pygame.font.SysFont("Arial", 20)
    text1 = f.render("F1: 1P mode with auto attack", 1, WHITE)
    text2 = f.render("F2: 1P mode with invisible blocks", 1, WHITE)
    text3 = f.render("F3: 4-wide practice", 1, WHITE)
    centerx, centery = screen.get_rect().center
    screen.fill(BLACK)
    screen.blit(text1, (centerx - 200, centery - 30))
    screen.blit(text2, (centerx - 200, centery     ))
    screen.blit(text3, (centerx - 200, centery + 30))
    pygame.display.flip()
    game = None
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT: sys.exit()
      if event.type == pygame.KEYDOWN:
        if event.key == K_F1:
          game = Game1P(screen)
        elif event.key == K_F2:
          game = Game1PInvisible(screen)
        elif event.key == K_F3:
          game = Game1P4W(screen)

    if game is not None:
      game.start()

    pygame.time.Clock().tick(120)

if __name__ == "__main__":
  main()
