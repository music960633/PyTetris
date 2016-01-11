import pygame
from mino import *
from util import *

'''   class Field definition   '''
class Field:
  def __init__(self, width, height, invisible = False):
    # width and height
    self.width  = width
    self.height = height
    # stacked piece invisible
    self.invisible = invisible
    # initial position of a piece
    self.mino_initpos = (self.width/2-1, self.height-1)
    # size of next queue
    self.next_size = 5

    self.restart()

  def restart(self):
    self.occupied = [[False]*self.height for i in range(self.width)]
    self.pattern = [[None]*self.height for i in range(self.height)]
    default_surface = [make_surface(BLACK), make_surface(GRAY)]
    self.default = [[default_surface[(i+j) % 2] for j in range(self.height)] for i in range(self.height)]
    # gameover flag
    self.gameover = False
    # mino pack generator
    self.generator = Generator()
    # next queue
    self.nextminos = [self.generator.next_mino() for x in range(self.next_size)]
    # current piece
    self.mino = self.pop_nextmino()
    # hold piece and hold flag
    self.hold = None
    self.holdflag = True
    # recieved attack buffer
    self.atk_buffer = []
   
    '''   game status   '''
    # line clear
    self.lineClear = 0
    # T-spin flag
    self.tSpin = False
    self.tSpinDisplay = False
    # line cleared total
    self.lineTotal = 0
    # attack total
    self.attackTotal = 0
    # combo count
    self.combo = 0
    # back to back
    self.b2b = False

  # returns a 2D array containing only True or False
  def get_map(self):
    return [[self.occupied[i][j] for j in range(self.width)] for i in range(self.height)]

  # get a new mino from the next queue
  def pop_nextmino(self):
    nextmino = self.nextminos[0]
    nextmino.moveto(self.mino_initpos)
    self.nextminos = self.nextminos[1:]
    self.nextminos.append(self.generator.next_mino())
    return nextmino

  # draw everything
  def draw(self):
    s_grid = self.drawGrid(RED if self.gameover else WHITE, 1)
    s_hold = self.drawHold(WHITE, 1)
    s_next = self.drawNext(WHITE, 1)
    s_buffer = self.drawBuffer(WHITE, 1)
    s_status = self.drawStatus(WHITE, 1)
    w_grid, h_grid = s_grid.get_size()
    w_hold, h_hold = s_hold.get_size()
    w_next         = s_next[0].get_width()
    w_buffer, h_buffer = s_buffer.get_size()

    surface = pygame.Surface((w_hold + w_grid + w_buffer + w_next + 3*SPACE_WIDTH, h_grid))
   
    # blit hold piece
    surface.blit(s_hold, (0, 0))
    # blit stacked piece and current piece
    surface.blit(s_grid, (w_hold + SPACE_WIDTH, 0))
    # blit attack buffer
    surface.blit(s_buffer, (w_hold + w_grid + 2*SPACE_WIDTH, 0))
    # blit next queue
    sum_h = 0
    for i in range(self.next_size):
      surface.blit(s_next[i], (w_hold + w_grid + w_buffer + 3*SPACE_WIDTH, sum_h))
      sum_h += s_next[i].get_height() + SPACE_WIDTH
    # blit status
    surface.blit(s_status, (0, 300))

    return surface
  
  # draw the grids
  def drawGrid(self, color, linewidth):
    surface = pygame.Surface((self.width*BLOCK_WIDTH, self.height*BLOCK_WIDTH))
    transform = lambda (x, y): (x*BLOCK_WIDTH, (self.height-y-1)*BLOCK_WIDTH)
    # current map
    for i in range(self.width):
      for j in range(self.height):
        if self.pattern[i][j] is not None:
          surface.blit(self.pattern[i][j], transform((i, j)))
        else:
          surface.blit(self.default[i][j], transform((i, j)))
    # ghost piece
    ghost = self.mino.ghost(self)
    for pos in ghost.get_pos():
      if self.check_inside(pos):
        surface.blit(ghost.pattern, transform(pos))
    # current piece
    for pos in self.mino.get_pos():
      if self.check_inside(pos):
        surface.blit(self.mino.pattern, transform(pos))
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
    f = pygame.font.SysFont("Consolas", 24)
    text1 = f.render("%4d lines  " % self.lineTotal, 2, WHITE)
    text2 = f.render("%4d attack " % self.attackTotal, 2, WHITE)
    text3 = f.render("%4d combo  " % self.combo, 2, WHITE)
    text4 = f.render(self.getClearDescription(self.lineClear, self.tSpinDisplay), 2, WHITE)
    w1, h1 = text1.get_size()
    w2, h2 = text2.get_size()
    w3, h3 = text3.get_size()
    w4, h4 = text4.get_size()
    surface = pygame.Surface((max(w1, w2, w3, w4), h1 + h2 + h3 + h4))
    surface.blit(text1, (0, 0))
    surface.blit(text2, (0, h1))
    surface.blit(text3, (0, h1 + h2))
    surface.blit(text4, (0, h1 + h2 + h3))
    # add frame
    surface = add_frame(surface, color, linewidth)
    return surface 

  # check if all the coordinates are inside the boundaries and are empty 
  # ** do not check upper bound
  def check_valid_list(self, posList):
    for pos in posList:
      if not self.check_valid(pos): return False
    return True
  
  # check if the coordinate is inside the boundaries and is empty
  # ** do not check upper bound
  def check_valid(self, (x, y)):
    if x < 0 or x >= self.width or y < 0: return False
    if y < self.height and self.occupied[x][y]: return False
    return True

  # check if the coordinate is inside the boundary
  def check_inside(self, (x, y)):
    return x >= 0 and x < self.width and y >= 0 and y < self.height

  # move the mino
  def moveMino(self, direction = (0, 0)):
    if self.gameover: return
    success = self.mino.move(direction, self)
    if success: self.tSpin = False
    return success
  
  # turn the mino
  def turnMino(self, rev = False):
    if self.gameover: return
    success = self.mino.turn(rev, self)
    if success: self.tSpin = self.checkTspin(self.mino)
    return success
  
  # harddrop the mino
  def dropMino(self):
    if self.gameover: return
    while self.moveMino((0, -1)): pass
    for x, y in self.mino.get_pos():
      if self.check_inside((x, y)):
        self.occupied[x][y] = True
        if self.invisible == False:
          self.pattern[x][y] = self.mino.pattern
    self.lineClear = self.clearAllLine()
    self.tSpinDisplay = self.tSpin
    attack, self.b2b = self.sendAttack(self.lineClear, self.tSpinDisplay, self.b2b, self.combo)
    self.lineTotal += self.lineClear
    self.attackTotal += attack
    if self.lineClear == 0:
      self.combo = 0
      self.clearAttack()
    else:
      self.combo += 1
      self.cancelAttack(attack)
    self.mino = self.pop_nextmino()
    self.holdflag = True
    # check game over
    if not self.check_valid_list(self.mino.get_pos()):
      self.gameover = True

  # hold the mino
  def holdMino(self):
    if self.gameover: return
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
    count = 0
    for row in range(self.height-1, -1, -1):
      if self.checkLine(row):
        self.clearLine(row)
        count += 1
    return count
  
  # check if the row should be cleared
  def checkLine(self, row):
    for i in range(self.width):
      if not self.occupied[i][row]: 
        return False
    return True 

  # clear a single line
  def clearLine(self, row):
    for j in range(row, self.height):
      for i in range(self.width):
        if j == self.height - 1:
          self.occupied[i][j] = False
          self.pattern[i][j] = None
        else:
          self.occupied[i][j] = self.occupied[i][j+1]
          self.pattern[i][j] = self.pattern[i][j+1]
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
            self.occupied[i][j] = self.occupied[i][j-atk]
            self.pattern[i][j] = self.pattern[i][j-atk]
          else:
            self.occupied[i][j] = False if i == hole else True
            self.pattern[i][j] = None if i == hole else make_surface(SILVER)
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
  def sendAttack(self, line, tspin, b2b, combo):
    # not T-spin
    if not tspin:
      if   line == 0: atk, b2b = 0, b2b
      elif line == 1: atk, b2b = 0, False
      elif line == 2: atk, b2b = 1, False
      elif line == 3: atk, b2b = 2, False
      elif line == 4:
        if b2b: atk, b2b = 5, True
        else:   atk, b2b = 4, True
      else: assert False, "line clear out of bound"
    # T-spin
    else:
      if   line == 0: atk, b2b = 0, b2b
      elif line == 1:
        if b2b: atk, b2b = 3, True
        else:   atk, b2b = 2, True
      elif line == 2:
        if b2b: atk, b2b = 5, True
        else  : atk, b2b = 4, True
      elif line == 3:
        if b2b: atk, b2b = 8, True
        else  : atk, b2b = 6, True
      else: assert False, "line clear out of bound"
    # combo
    if combo <= 1: atk += 0
    elif combo <= 3: atk += 1
    elif combo <= 5: atk += 2
    elif combo <= 7: atk += 3
    else: atk += 4
    return atk, b2b

  # line clear description string
  def getClearDescription(self, line, tspin):
    assert 0 <= line <= 4
    table = ["", "single", "double", "triple", "tetris"]
    s = "  T " if tspin else "  "
    s += table[line]
    return s
  
  # check T spin
  def checkTspin(self, mino):
    if not mino.isT: return False
    centerx, centery = mino.center
    counter = 0
    for dx, dy in [(1, 1), (1, -1), (-1, -1), (-1, 1)]:
      if not self.check_valid((centerx + dx, centery + dy)):
        counter += 1
    return counter >= 3

