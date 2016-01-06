import pygame
from game import *

def main():
  pygame.init()
  pygame.display.set_caption("PyTetris")
  screen = pygame.display.set_mode(SCREEN_SIZE)
  
  game = GameInvisible(screen)
  game.start()

if __name__ == "__main__":
  main()
