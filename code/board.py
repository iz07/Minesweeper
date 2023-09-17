from random import randint
from util import *
from settings import *

from tile import Tile

class Board:
  def __init__(self) -> None:
    self.mines = []
    self.tiles = [[] for x in range(BOARD_HEIGHT)]
    self.cd = 0
    self.flag = load_image('flag', 4)
    
    for r in range(0, BOARD_HEIGHT):
      for c in range(0, BOARD_WIDTH):
        tile_surface = load_image('grass_' + str(randint(1,4)), 4)
        tile_rect = tile_surface.get_rect(topleft = (c * TILE_SIZE, r * TILE_SIZE))
        tile = Tile(tile_surface, tile_rect)
        self.tiles[r].append(tile)
  
  def load_data(self, first_click):
    # space where mines shouldn't be generated
    invalid_mines = [
      (first_click[0] - 1, first_click[1] - 1),
      (first_click[0] - 1, first_click[1]),
      (first_click[0] - 1, first_click[1] + 1),
      (first_click[0] + 1, first_click[1] - 1),
      (first_click[0] + 1, first_click[1]),
      (first_click[0] + 1, first_click[1] + 1),
      (first_click[0], first_click[1] - 1),
      (first_click[0], first_click[1] + 1)
    ]

    # Generate Mines
    while len(self.mines) < MINE_COUNT:
      r, c = randint(0,BOARD_WIDTH - 1), randint(0, BOARD_HEIGHT - 1)
      if (r, c) not in self.mines and (r, c) not in invalid_mines:
        self.mines.append((r, c))

    for r in range(0, BOARD_HEIGHT):
      for c in range(0, BOARD_WIDTH):
        if (r, c) in self.mines:
          count = -1
        else:
          count = self.count_mines(r,c)
        self.tiles[r][c].set_mines_nearby(count)

  def count_mines(self, r, c):
    count = 0
    # Check all surrounding tiles
    if (r - 1, c - 1) in self.mines: count += 1
    if (r - 1, c) in self.mines: count += 1
    if (r - 1, c + 1) in self.mines: count += 1
    if (r + 1, c - 1) in self.mines: count += 1
    if (r + 1, c) in self.mines: count += 1
    if (r + 1, c + 1) in self.mines: count += 1
    if (r, c - 1) in self.mines: count += 1
    if (r, c + 1) in self.mines: count += 1

    return count
  
  def clear_flags(self):
    for row in self.tiles:
      for tile in row:
        tile.flagged = False

  def render(self, screen):
    all_tiles_flipped = True
    for row in self.tiles:
      for tile in row:
        screen.blit(tile.surface, tile.rect)
        if tile.mines_nearby > -1 and not tile.flipped:
          all_tiles_flipped = False
        if tile.flagged:
          screen.blit(self.flag, tile.rect)
    return all_tiles_flipped

  def flip_mines(self):
    for mine in self.mines:
      self.tiles[mine[0]][mine[1]].surface = load_image('mine', 4)

  def flip_tile(self, r, c):
    # RETURN IF TILE IS:
    # - OUT OF BOUNDS
    # - ALREADY FLIPPED
    # - A MINE
    if not (0 <= r < BOARD_WIDTH) or not (0 <= c < BOARD_HEIGHT) or self.tiles[r][c].flipped or (r, c) in self.mines:
      return
    # Flip tile
    self.tiles[r][c].flip_tile()
    # If the tile has mines nearby, only flip this tile
    if self.tiles[r][c].mines_nearby > 0:
      return
      
    # Tile has no mines nearby, flip every tile in its surroundings
    self.flip_tile(r - 1, c - 1)
    self.flip_tile(r - 1, c)
    self.flip_tile(r - 1, c + 1)
    self.flip_tile(r + 1, c - 1)
    self.flip_tile(r + 1, c)
    self.flip_tile(r + 1, c + 1)
    self.flip_tile(r, c - 1)
    self.flip_tile(r, c + 1)

  def flag_tile(self, r, c):
    if not self.tiles[r][c].flipped:
      self.tiles[r][c].trigger_flag()

