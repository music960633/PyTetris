import pygame

'''   class KeyHandler definition   '''
# handles keyboard input
class KeyHandler:
  class KeyInfo:
    def __init__(self, repeat, delay, rate):
      self.time = 0
      self.status = 0
      self.repeat = repeat
      self.delay = delay
      self.rate = rate

  def __init__(self):
    self.target = {}
  
  # add a key
  def addKey(self, key, repeat, delay = 1, rate = 1):
    self.target[key] = self.KeyInfo(repeat, delay, rate)

  # get triggered key
  def getTrigger(self, time):
    press = pygame.key.get_pressed()
    trigger = []
    for key in self.target:
      info = self.target[key]
      if press[key] == 1:
        info.time += time
        if info.status == 0:
          info.status = 1
          trigger.append(key)
        elif info.status == 1 and info.repeat:
          if info.time >= info.delay:
            info.time = 0
            info.status = 2
            trigger.append(key)
        elif info.status == 2 and info.repeat:
          if info.time >= info.rate:
            info.time = 0
            trigger.append(key)
      else:
        info.time = 0
        info.status = 0
    return trigger

