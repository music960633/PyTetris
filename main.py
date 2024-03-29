import sys
import pygame
from pygame.locals import *
from game import Game1pNormal, Game1pInvisible, Game1pDig, Game1p4wide
from menu import Menu
from defines import *

def main():
  pygame.init()
  pygame.display.set_caption("PyTetris")
  screen = pygame.display.set_mode(SCREEN_SIZE)
  
  menu_main = build_menu()
  menu_main.start()
  
def build_menu():
  # 1P menu
  menu_1P = Menu() 
  menu_1P.addOption("1P mode with auto attack", Game1pNormal().start)
  menu_1P.addOption("1P mode with invisible blocks", Game1pInvisible().start)
  
  # practice menu
  menu_prac = Menu()
  menu_prac.addOption("4-wide practice", Game1p4wide().start)
  menu_prac.addOption("dig challenge", Game1pDig().start)
  menu_prac.addOption("dig challenge (classic)", Game1pDig(False, 'classic', 1000, 1).start)

  # main menu
  menu_main = Menu(isRoot = True)
  menu_main.addOption("1 player", menu_1P.start)
  menu_main.addOption("Practice", menu_prac.start)

  return menu_main


if __name__ == "__main__":
  main()
