import pygame
from mino import *

'''   class Field definition   '''
class Field:
  def __init__(self, width, height, w_offset=0, h_offset=0):
    self.width  = width
    self.height = height
    self.w_offset = w_offset
    self.h_offset = h_offset
    self.mino_initpos = (self.width/2-1, self.height-1)
    self.restart()

  def restart(self):
    self.frame  = pygame.Rect(self.w_offset-1, self.h_offset-1, self.width*BLOCK_WIDTH+2, self.height*BLOCK_WIDTH+2)
    self.blocks = [[        \
      {                     \
        "occupied": False,  \
        "pattern" : None,   \
        "default" : make_surface(BLACK if (i+j) % 2 == 0 else GRAY) \
      }                     \
      for j in range(self.height)] for i in range(self.width)]
    
    self.generator = Generator()
    self.mino = self.generator.next_mino(self.mino_initpos)
    self.nextminos = [self.generator.next_mino(self.mino_initpos) for x in range(3)]
    self.holdflag = True
    self.hold = None

    self.clear_row = []
    self.clear_effect = 0

  # returns True if blocked by some effects (cannot move the mino)
  def pause(self):
    return self.clear_effect > 0

  # map grid index to coordinates
  def transform(self, (x, y)):
    return (x*BLOCK_WIDTH + self.w_offset, (self.height-1-y)*BLOCK_WIDTH + self.h_offset)

  # returns a 2D array containing only True or False
  def get_map(self):
    return [[self.blocks["occupied"] for j in range(self.width)] for i in range(self.height)]

  # draw everything
  def draw(self, surface):
    self.drawGrid(surface)
    self.drawMino(surface)
    self.drawHold(surface)
    self.drawNext(surface)

    self.FX_clearLine(surface)
  
  # draw the grids
  def drawGrid(self, surface):
    pygame.draw.rect(surface, WHITE, self.frame, 1)
    for i in range(self.width):
      for j in range(self.height):
        block = self.blocks[i][j]
        if block["pattern"] is not None:
          surface.blit(block["pattern"], self.transform((i, j)))
        else:
          surface.blit(block["default"], self.transform((i, j)))

  # draw the mino and ghost piece
  def drawMino(self, surface):
    # ghost piece
    ghost = self.mino.ghost(self)
    for pos in ghost.get_pos():
      if self.check_inside(pos):
        surface.blit(ghost.pattern, self.transform(pos))
    # current piece
    for pos in self.mino.get_pos():
      if self.check_inside(pos):
        surface.blit(self.mino.pattern, self.transform(pos))

  # draw the hold piece
  def drawHold(self, surface):
    if self.hold is not None:
      for x, y in self.hold.get_pos():
        surface.blit(self.hold.pattern, self.transform((x - self.width/2 - 3, y - 4)))
  
  # draw the next pieces
  def drawNext(self, surface):
    for i in range(len(self.nextminos)):
      nextmino = self.nextminos[i]
      for x, y in nextmino.get_pos():
        surface.blit(nextmino.pattern, self.transform((x + self.width/2 + 3, y - 4*i - 4)))

  # clear line effect (blocking)
  def FX_clearLine(self, surface):
    if self.clear_effect <= 0: return
    c = self.clear_effect
    self.clear_effect -= 20
    for row in self.clear_row:
      for i in range(self.width):
        surface.blit(make_surface((c, c, c)), self.transform((i, row)))
    if self.clear_effect <= 0: 
      for row in self.clear_row:
        self.clearLine(row)
      self.clear_row = []

  # check if all the coordinates are inside the boundaries and are empty 
  # **(do not check upper bound)
  def check_valid(self, posList):
    for x, y in posList:
      if x < 0 or x >= self.width or y < 0: return False
      if y < self.height and self.blocks[x][y]["occupied"]: return False
    return True

  # check if the coordinate is inside the boundary
  def check_inside(self, (x, y)):
    return x >= 0 and x < self.width and y >= 0 and y < self.height

  # move the mino
  def moveMino(self, direction = (0, 0)):
    if self.pause(): return False
    return self.mino.move(direction, self)
  
  # turn the mino
  def turnMino(self, rev = False):
    if self.pause(): return False
    return self.mino.turn(rev, self)
  
  # harddrop the mino
  def dropMino(self):
    if self.pause(): return False
    while self.moveMino((0, -1)): pass
    for x, y in self.mino.get_pos():
      if self.check_inside((x, y)):
        self.blocks[x][y]["occupied"] = True
        self.blocks[x][y]["pattern"] = self.mino.pattern
    self.clearAllLine()
    self.mino = self.pop_nextmino()
    self.holdflag = True

  # hold the mino
  def holdMino(self):
    if self.holdflag == True:
      tmp = self.hold
      self.hold = self.mino
      self.hold.moveto(self.mino_initpos)
      self.mino = tmp
      if self.mino == None:
        self.mino = self.pop_nextmino()
      self.holdflag = False
      
  # clear all lines
  def clearAllLine(self):
    if self.pause(): return
    for row in range(self.height-1, -1, -1):
      if self.checkLine(row):
        self.clear_row.append(row)
        self.clear_effect = 200
  
  # check if the row should be cleared
  def checkLine(self, row):
    for i in range(self.width):
      if not self.blocks[i][row]["occupied"]: 
        return False
    return True 

  # clear a single line
  def clearLine(self, row):
    for j in range(row, self.height):
      for i in range(self.width):
        if j == self.height - 1:
          self.blocks[i][j]["occupied"] = False
          self.blocks[i][j]["pattern"] = None
        else:
          self.blocks[i][j]["occupied"] = self.blocks[i][j+1]["occupied"]
          self.blocks[i][j]["pattern"] = self.blocks[i][j+1]["pattern"]
    return True

  # get a new mino from the next queue
  def pop_nextmino(self):
    nextmino = self.nextminos[0]
    size = len(self.nextminos)
    self.nextminos = self.nextminos[1:]
    self.nextminos.append(self.generator.next_mino(self.mino_initpos))
    return nextmino

