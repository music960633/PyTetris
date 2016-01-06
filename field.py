import pygame
from mino import *
from util import *

'''   class Field definition   '''
class Field:
  def __init__(self, width, height, w_offset=0, h_offset=0):
    self.width  = width
    self.height = height
    self.w_offset = w_offset
    self.h_offset = h_offset
    self.mino_initpos = (self.width/2-1, self.height-1)
    self.next_size = 5

    self.invisible = False
    self.restart()

  def restart(self, invisible = False):
    self.invisible = invisible
    self.blocks = [[        \
      {                     \
        "occupied": False,  \
        "pattern" : None,   \
        "default" : make_surface(BLACK if (i+j) % 2 == 0 else GRAY) \
      }                     \
      for j in range(self.height)] for i in range(self.width)]
    
    self.generator = Generator()
    self.nextminos = [self.generator.next_mino() for x in range(self.next_size)]
    self.mino = self.pop_nextmino()
    self.holdflag = True
    self.hold = None
    self.atk_buffer = []

    self.linecount = 0

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

  # get a new mino from the next queue
  def pop_nextmino(self):
    nextmino = self.nextminos[0]
    nextmino.moveto(self.mino_initpos)
    self.nextminos = self.nextminos[1:]
    self.nextminos.append(self.generator.next_mino())
    return nextmino

  # draw everything
  def draw(self):
    s_grid = self.drawGrid(WHITE, 1)
    s_hold = self.drawHold(WHITE, 1)
    s_next = self.drawNext(WHITE, 1)
    s_buffer = self.drawBuffer(WHITE, 1)
    s_status = self.drawStatus(WHITE, 1)
    w_grid, h_grid = s_grid.get_size()
    w_hold, h_hold = s_hold.get_size()
    w_next, h_next = s_hold.get_size()
    w_buffer, h_buffer = s_buffer.get_size()

    surface = pygame.Surface((w_hold + w_grid + w_buffer + w_next + 3*SPACE_WIDTH, max(h_grid, h_next)))
    
    surface.blit(s_hold, (0, 0))
    surface.blit(s_grid, (w_hold + SPACE_WIDTH, 0))
    surface.blit(s_buffer, (w_hold + w_grid + 2*SPACE_WIDTH, 0))
    sum_h = 0
    for i in range(self.next_size):
      surface.blit(s_next[i], (w_hold + w_grid + w_buffer + 3*SPACE_WIDTH, sum_h))
      sum_h += s_next[i].get_height() + SPACE_WIDTH
    surface.blit(s_status, (0, 300))

    return surface
  
  # draw the grids
  def drawGrid(self, color, linewidth):
    surface = pygame.Surface((self.width*BLOCK_WIDTH, self.height*BLOCK_WIDTH))
    transform = lambda (x, y): (x*BLOCK_WIDTH, (self.height-y-1)*BLOCK_WIDTH)
    # current map
    for i in range(self.width):
      for j in range(self.height):
        block = self.blocks[i][j]
        if block["pattern"] is not None:
          surface.blit(block["pattern"], transform((i, j)))
        else:
          surface.blit(block["default"], transform((i, j)))
    # ghost piece
    ghost = self.mino.ghost(self)
    for pos in ghost.get_pos():
      if self.check_inside(pos):
        surface.blit(ghost.pattern, transform(pos))
    # current piece
    for pos in self.mino.get_pos():
      if self.check_inside(pos):
        surface.blit(self.mino.pattern, transform(pos))
    # clear line effect
    if self.clear_effect > 0:
      c = self.clear_effect
      self.clear_effect -= 20
      for row in self.clear_row:
        for i in range(self.width):
          surface.blit(make_surface((c, c, c)), self.transform((i, row)))
      if self.clear_effect <= 0: 
        for row in self.clear_row:
          self.clearLine(row)
        self.clear_row = []
    # add frame
    surface = add_frame(surface, color, linewidth)
    return surface

  # draw the hold piece
  def drawHold(self, color, linewidth):
    surface = pygame.Surface((4*BLOCK_WIDTH, 4*BLOCK_WIDTH))
    transform = lambda (x, y): (x*BLOCK_WIDTH, (3-y)*BLOCK_WIDTH)
    # hold piece
    if self.hold is not None:
      fx, fy = 2*BLOCK_WIDTH, 2*BLOCK_WIDTH
      cx, cy = find_center(self.hold.get_pos())
      for x, y in self.hold.get_pos():
        surface.blit(self.hold.pattern, (int(fx + (x-cx-0.5)*BLOCK_WIDTH), int(fy + (-y+cy-0.5)*BLOCK_WIDTH)))
    # resize to hold size
    surface = pygame.transform.scale(surface, HOLD_SIZE)
    # add frame
    surface = add_frame(surface, color, linewidth)
    return surface
  
  # draw the next pieces
  def drawNext(self, color, linewidth):
    surfaceList = []
    transform = lambda (x, y): (x*BLOCK_WIDTH, (3-y)*BLOCK_WIDTH)
    for i in range(self.next_size):
      nextmino = self.nextminos[i]
      surface = pygame.Surface((4*BLOCK_WIDTH, 4*BLOCK_WIDTH))
      fx, fy = 2*BLOCK_WIDTH, 2*BLOCK_WIDTH
      cx, cy = find_center(nextmino.get_pos())
      for x, y in nextmino.get_pos():
        surface.blit(nextmino.pattern, (int(fx + (x-cx-0.5)*BLOCK_WIDTH), int(fy + (-y+cy-0.5)*BLOCK_WIDTH)))
      # resize to next size
      surface = pygame.transform.scale(surface, NEXT_SIZE)
      # add frame
      surface = add_frame(surface, color, linewidth)
      # add to list
      surfaceList.append(surface)
    return surfaceList

  def drawBuffer(self, color, linewidth):
    surface = pygame.Surface((BUFFER_WIDTH, self.height*BLOCK_WIDTH))
    transform = lambda y: (0, (self.height-1-y)*BLOCK_WIDTH)
    buffer_sum = sum(self.atk_buffer)
    for i in range(min(buffer_sum, self.height)):
      bar = make_surface(RED, (BUFFER_WIDTH, BLOCK_WIDTH))
      surface.blit(bar, transform(i))
    # add frame
    surface = add_frame(surface, color, linewidth)
    return surface
  
  def drawStatus(self, color, linewidth):
    f = pygame.font.SysFont("Consolas", 30)
    surface = f.render("%3d lines" % self.linecount, 2, WHITE)
    # add frame
    surface = add_frame(surface, color, linewidth)
    return surface 

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
        if self.invisible == False:
          self.blocks[x][y]["pattern"] = self.mino.pattern
    clear_count = self.clearAllLine()
    if clear_count == 0:
      self.clearAttack()
    else:
      self.linecount += clear_count
      self.cancelAttack(self.sendAttack(clear_count))
    self.mino = self.pop_nextmino()
    self.holdflag = True

  # hold the mino
  def holdMino(self):
    if self.holdflag == True:
      tmp = self.hold
      self.hold = self.mino
      self.hold.moveto((0, 0))
      self.hold.turnto(0)
      self.mino = tmp
      if self.mino == None:
        self.mino = self.pop_nextmino()
      else:
        self.mino.moveto(self.mino_initpos)
      self.holdflag = False
      
  # clear all lines
  def clearAllLine(self):
    if self.pause(): return
    count = 0
    for row in range(self.height-1, -1, -1):
      if self.checkLine(row):
        self.clear_row.append(row)
        self.clear_effect = 200
        count += 1
    return count
  
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
  
  # recieve line (add to buffer)
  def recieveAttack(self, atk):
    self.atk_buffer.append(atk)

  # push line and clear buffer
  def clearAttack(self):
    for atk in self.atk_buffer:
      hole = random.randint(0, self.width-1)
      for j in range(self.height-1, -1, -1):
        for i in range(self.width):
          if j >= atk:
            self.blocks[i][j]["occupied"] = self.blocks[i][j-atk]["occupied"]
            self.blocks[i][j]["pattern"] = self.blocks[i][j-atk]["pattern"]
          else:
            self.blocks[i][j]["occupied"] = False if i == hole else True
            self.blocks[i][j]["pattern"] = None if i == hole else make_surface(SILVER)
    self.atk_buffer = []

  # cancel attack
  def cancelAttack(self, val):
    while len(self.atk_buffer) > 0 and val > 0:
      atk = self.atk_buffer[-1]
      self.atk_buffer.pop()
      if val >= atk:
        val -= atk
      else:
        self.atk_buffer.append(atk - val)
        val = 0
    return val

  # send attack
  def sendAttack(self, line):
    if line == 0: return 0
    elif line == 1: return 0
    elif line == 2: return 1
    elif line == 3: return 2
    elif line == 4: return 4
    else: return 0
