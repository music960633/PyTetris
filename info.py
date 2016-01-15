'''   class GameInfo definition   '''
class GameInfo:
  def __init__(self):
    self.lineTot = 0
    self.atkTot  = 0
    self.combo   = 0
    self.b2b     = False

  def updateAndGetAtk(self, line, tspin):
    atk = self.calcAtk(line, tspin)
    self.lineTot += line
    self.atkTot += self.calcAtk(line, tspin)
    self.combo = (self.combo + 1) if line > 0 else 0
    self.b2b = self.b2b if line == 0 else (line == 4 or tspin)
    return atk

  def calcAtk(self, line, tspin):
    clearAtk = 0
    # normal attack
    if not tspin:
      assert 0 <= line <= 4, "invalid lines"
      if not self.b2b:
        clearAtk = (0, 0, 1, 2, 4)[line]
      else:
        clearAtk = (0, 0, 1, 2, 5)[line]
    # T spin attack
    else:
      assert 0 <= line <= 3, "invalid lines"
      if not self.b2b:
        clearAtk = (0, 2, 4, 6)[line]
      else:
        clearAtk = (0, 3, 5, 8)[line]
    # combo attack
    if self.combo < 8:
      comboAtk = (0, 0, 1, 1, 2, 2, 3, 3)[self.combo]
    else:
      comboAtk = 4
    return clearAtk + comboAtk

