'''   class GameInfo definition   '''
class GameInfo:
  def __init__(self):
    self.lineTot = 0
    self.atkTot  = 0
    self.combo   = 0
    self.b2b     = True

  def getInfo(self):
    return self.lineTot, self.atkTot, self.combo, self.b2b

  def getLine(self):
    return self.lineTot

  def getAtk(self):
    return self.atkTot

  def getCombo(self):
    return self.combo

  def getB2b(self):
    return self.b2b

  def update(self, line, atk, tspin):
    self.lineTot += line
    self.atkTot  += atk
    self.combo   = (self.combo + 1) if line > 0 else 0
    self.b2b     = True if (line == 4 or tspin) else False
