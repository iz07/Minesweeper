from util import *

class Tile():
  # if mines_nearby = -1, this tile is a mine
  def __init__(self, surface, rect, mines_nearby = 0) -> None:
    self.surface = surface
    self.rect = rect
    self.mines_nearby = mines_nearby
    self.flagged = False
    self.flipped = False
    self.font = load_font('LycheeSoda')

  def flip_tile(self):
    if self.mines_nearby > -1:
      self.surface = load_image('dirt_' + str(self.mines_nearby), 4)
      self.flipped = True

  def trigger_flag(self):
    self.flagged = not self.flagged

  def set_mines_nearby(self, num):
    self.mines_nearby = num
    

