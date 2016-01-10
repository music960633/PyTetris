import sys
import pygame
from pygame.locals import *
from game import *
from menu import *
from defines import *

def main():
  pygame.init()
  pygame.display.set_caption("PyTetris")
  screen = pygame.display.set_mode(SCREEN_SIZE)
  
  menu = Menu(isRoot = True)
  menu.addOption("1P mode with auto attack"     , Game1P(screen).start)
  menu.addOption("1P mode with invisible blocks", Game1PInvisible(screen).start)
  menu.addOption("4-wide practice"              , Game1P4W(screen).start)
  menu.start()

if __name__ == "__main__":
  main()
