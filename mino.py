import pygame
import random
from defines import *

'''   class Mino definition   '''
class Mino:
  def __init__(self, center, pos, orientation, turn_enable, turn_center, turn_table, pattern):
    self.center       = center
    self.pos          = list(pos)
    self.orientation  = orientation
    self.turn_enable  = turn_enable
    self.turn_center  = turn_center
    self.turn_table   = turn_table
    self.pattern      = pattern
  
  # create an identical Mino (with different center position)
  def copy(self, center = None):
    if center == None:
      center = self.center
    return Mino(center, self.pos, self.orientation, self.turn_enable, self.turn_center, self.turn_table, self.pattern)

  # get the absolute positions of the mino
  def get_pos(self):
    return [(x+self.center[0], y+self.center[1]) for x, y in self.pos]
  
  # move the mino, return False if fails
  def move(self, (dirx, diry), field = None):
    next_center = (self.center[0] + dirx, self.center[1] + diry)
    abs_pos = [(x + next_center[0], y + next_center[1]) for x, y in self.pos]
    if field == None or field.check_valid(abs_pos):
      self.center = next_center
      return True
    return False

  # turn the mino, return False if fails
  def turn(self, rev, field = None):
    if not self.turn_enable: return False
    if not rev:
      next_orientation = (self.orientation + 1) % 4
      next_pos = [(y + self.turn_center[0][0], -x + self.turn_center[0][1]) for x, y in self.pos]
      test_table = self.turn_table[0][self.orientation]
    else:       
      next_orientation = (self.orientation + 3) % 4
      next_pos = [(-y + self.turn_center[1][0], x + self.turn_center[1][1]) for x, y in self.pos]
      test_table = self.turn_table[1][self.orientation]
    for test_x, test_y in test_table:
      next_center = (self.center[0] + test_x, self.center[1] + test_y)
      abs_pos = [(next_center[0] + x, next_center[1] + y) for x, y in next_pos]
      if field == None or field.check_valid(abs_pos):
        self.center, self.orientation, self.pos = next_center, next_orientation, next_pos
        return True
    return False
  
  # move the center do not check any boundaries
  def moveto(self, center):
    self.center = center

  def turnto(self, orientation):
    assert 0 <= orientation < 4, "orientation is not 0~3"
    while self.orientation != orientation:
      self.turn(False)

  # returns a ghost piece
  def ghost(self, field):
    mino = self.copy()
    mino.pattern = make_surface(GHOST)
    while mino.move((0, -1), field): pass
    return mino

'''   SRS tables   '''
# table for T, J, L, S, Z
SRS_TJLSZ = \
( \
  # clockwise \
  (   \
    [(0, 0), (-1, 0), (-1,  1), (0, -2), (-1, -2)], \
    [(0, 0), ( 1, 0), ( 1, -1), (0,  2), ( 1,  2)], \
    [(0, 0), ( 1, 0), ( 1,  1), (0, -2), ( 1, -2)], \
    [(0, 0), (-1, 0), (-1, -1), (0,  2), (-1,  2)]  \
  ),  \
  # counter-clockwise \
  (   \
    [(0, 0), ( 1, 0), ( 1,  1), (0, -2), ( 1, -2)], \
    [(0, 0), ( 1, 0), ( 1, -1), (0,  2), ( 1,  2)], \
    [(0, 0), (-1, 0), (-1,  1), (0, -2), (-1, -2)], \
    [(0, 0), (-1, 0), (-1, -1), (0,  2), (-1,  2)]  \
  )   \
)

# table for I
SRS_I = \
( \
  # clockwise \
  (   \
    [(0, 0), (-2, 0), ( 1, 0), (-2, -1), ( 1,  2)], \
    [(0, 0), (-1, 0), ( 2, 0), (-1,  2), ( 2, -1)], \
    [(0, 0), ( 2, 0), (-1, 0), ( 2,  1), (-1, -2)], \
    [(0, 0), ( 1, 0), (-2, 0), ( 1, -2), (-2,  1)]  \
  ),  \
  (   \
    [(0, 0), (-1, 0), ( 2, 0), (-1,  2), ( 2, -1)], \
    [(0, 0), ( 2, 0), (-1, 0), ( 2,  1), (-1, -2)], \
    [(0, 0), ( 1, 0), (-2, 0), ( 1, -2), (-2,  1)], \
    [(0, 0), (-2, 0), ( 1, 0), (-2, -1), ( 1,  2)]  \
  )   \
)

'''   functions that generate different Minos   '''
def Mino_I(center):
  return Mino(                                        \
    center      = center,                             \
    pos         = [(-1, 0), (0, 0), (1, 0), (2, 0)],  \
    orientation = 0,                                  \
    turn_enable = True,                               \
    turn_center = ((1, 0), (0, -1)),                  \
    turn_table  = SRS_I,                              \
    pattern     = make_surface(CYAN)                  \
)
def Mino_O(center):
  return Mino(                                        \
    center      = center,                             \
    pos         = [(0, 0), (0, 1), (1, 0), (1, 1)],   \
    orientation = 0,                                  \
    turn_enable = False,                              \
    turn_center = ((0, 0), (0, 0)),                   \
    turn_table  = None,                               \
    pattern     = make_surface(YELLOW)                \
)
def Mino_T(center):
  return Mino(                                        \
    center      = center,                             \
    pos         = [(-1, 0), (0, 0), (1, 0), (0, 1)],  \
    orientation = 0,                                  \
    turn_enable = True,                               \
    turn_center = ((0, 0), (0, 0)),                   \
    turn_table  = SRS_TJLSZ,                          \
    pattern     = make_surface(MAGENTA)               \
)
def Mino_J(center):
  return Mino(                                        \
    center      = center,                             \
    pos         = [(-1, 1), (-1, 0), (0, 0), (1, 0)], \
    orientation = 0,                                  \
    turn_enable = True,                               \
    turn_center = ((0, 0), (0, 0)),                   \
    turn_table  = SRS_TJLSZ,                          \
    pattern     = make_surface(BLUE)                  \
)
def Mino_L(center):
  return Mino(                                        \
    center      = center,                             \
    pos         = [(-1, 0), (0, 0), (1, 0), (1, 1)],  \
    orientation = 0,                                  \
    turn_enable = True,                               \
    turn_center = ((0, 0), (0, 0)),                   \
    turn_table  = SRS_TJLSZ,                          \
    pattern     = make_surface(ORANGE)                \
)
def Mino_S(center):
  return Mino(                                        \
    center      = center,                             \
    pos         = [(-1, 0), (0, 0), (0, 1), (1, 1)],  \
    orientation = 0,                                  \
    turn_enable = True,                               \
    turn_center = ((0, 0), (0, 0)),                   \
    turn_table  = SRS_TJLSZ,                          \
    pattern     = make_surface(RED)                   \
)
def Mino_Z(center):
  return Mino(                                        \
    center      = center,                             \
    pos         = [(-1, 1), (0, 1), (0, 0), (1, 0)],  \
    orientation = 0,                                  \
    turn_enable = True,                               \
    turn_center = ((0, 0), (0, 0)),                   \
    turn_table  = SRS_TJLSZ,                          \
    pattern     = make_surface(GREEN)                 \
)


'''   class Generator definition   '''
# mino pack generator
class Generator:
  def __init__(self):
    self.minos = [Mino_I, Mino_O, Mino_T, Mino_J, Mino_L, Mino_S, Mino_Z]
    self.reset()

  def reset(self):
    self.idx = [x for x in range(len(self.minos))]
    random.shuffle(self.idx)

  def next_mino(self, center = (0, 0)):
    mino = self.minos[self.idx[0]](center)
    self.idx = self.idx[1:]
    if len(self.idx) == 0:
      self.reset()
    return mino

