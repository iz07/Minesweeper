from random import randint
from util import *
from settings import *

from tile import Tile
from states.state import State

class Board(State):
  def __init__(self, game) -> None:
    super().__init__(game)
    
    self.w = DIFFICULTIES[self.game.difficulty][0]
    self.h = DIFFICULTIES[self.game.difficulty][1]
    self.num_mines = DIFFICULTIES[self.game.difficulty][2]

    self.mines = []
    self.tiles = [[] for x in range(self.h)]
    self.first_move = True
    self.flag = load_image('flag', IMAGE_SCALE)
    self.font = load_font('LycheeSoda')
    self.start_time = 0
    self.flag_count = self.num_mines
    
    for r in range(0, self.h):
      for c in range(0, self.w):
        tile_surface = load_image('grass_' + str(randint(1,4)), IMAGE_SCALE)
        tile_rect = tile_surface.get_rect(topleft = ((c + (BOARD_WIDTH - self.w)//2) * TILE_SIZE, (r + UI_HEIGHT) * TILE_SIZE))
        tile = Tile(tile_surface, tile_rect)
        self.tiles[r].append(tile)
      
  def update(self, actions):
    if self.game.playing and pygame.time.get_ticks() - self.game.click_icd > 200:
      if actions['lmb']:
        self.game.click_icd = pygame.time.get_ticks()
        pos = pygame.mouse.get_pos()
        c, r = pos[0] // TILE_SIZE, pos[1] // TILE_SIZE
        c -= (BOARD_WIDTH - self.w)//2
        r -= UI_HEIGHT
        # This is the first click, create board around this point
        if self.first_move:
          self.start_time = pygame.time.get_ticks()
          self.first_move = False
          self.load_data((r, c))
        if self.tiles[r][c].flagged:
          pass
        # Player has clicked on a mine, game over
        elif self.tiles[r][c].mines_nearby == -1:
          self.clear_flags()
          self.flip_mines()
          self.start_time = pygame.time.get_ticks()
          self.game.playing = False
        else: self.flip_tile(r, c)
      elif actions['rmb']:
        self.game.click_icd = pygame.time.get_ticks()
        # right click for flags
        self.click_icd = pygame.time.get_ticks()
        pos = pygame.mouse.get_pos()
        c, r = pos[0] // TILE_SIZE, pos[1] // TILE_SIZE
        c -= (BOARD_WIDTH - self.w)//2
        r -= UI_HEIGHT
        self.flag_tile(r, c)
    elif not self.game.playing:
      if actions['space']:
        self.exit_state()
        self.game.playing = True
        new_state = Board(self.game)
        new_state.enter_state()
    if actions['esc']:
      self.exit_state()
      self.game.playing = True
  
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
      (first_click[0], first_click[1]),
      (first_click[0], first_click[1] + 1)
    ]

    # Generate Mines
    while len(self.mines) < self.num_mines:
      r, c = randint(0,self.h - 1), randint(0, self.w - 1)
      if (r, c) not in self.mines and (r, c) not in invalid_mines:
        self.mines.append((r, c))

    for r in range(0, self.h):
      for c in range(0, self.w):
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

  def render(self, display):
    all_tiles_flipped = True

    display.fill((82, 126, 129))

    for row in self.tiles:
      for tile in row:
        display.blit(tile.surface, tile.rect)
        if tile.mines_nearby > -1 and not tile.flipped:
          all_tiles_flipped = False
        if tile.flagged:
          display.blit(self.flag, tile.rect)

    if self.first_move or not self.game.playing:
      time = f'Time: {self.start_time // 1000}'
    else:
      time = f'Time: {(pygame.time.get_ticks() - self.start_time) // 1000}'

    draw_text(display, self.font, time, 'White', SCREEN_WIDTH//2, int(TILE_SIZE))
    draw_text(display, self.font, f'Flags left: {self.flag_count}', 'White', SCREEN_WIDTH//2, int(TILE_SIZE * 2))

    if all_tiles_flipped: 
      self.game.playing = False
      self.start_time = pygame.time.get_ticks()
    
    if not self.game.playing:
      if all_tiles_flipped:
        draw_text(display, self.font, 'You win!', 'White', SCREEN_WIDTH//2, (self.h//2) * TILE_SIZE)
        draw_text(display, self.font, 'Press space to play again', 'White', SCREEN_WIDTH//2, (self.h//2) * TILE_SIZE + 40)
      else:
        draw_text(display, self.font, 'You lose', 'White', SCREEN_WIDTH//2, (self.h//2) * TILE_SIZE)
        draw_text(display, self.font, 'Press space to play again', 'White', SCREEN_WIDTH//2, (self.h//2) * TILE_SIZE + 40)

  def flip_mines(self):
    for mine in self.mines:
      self.tiles[mine[0]][mine[1]].surface = load_image('mine', IMAGE_SCALE)

  def flip_tile(self, r, c):
    # RETURN IF TILE IS:
    # - OUT OF BOUNDS
    # - ALREADY FLIPPED
    # - A MINE
    if not (0 <= r < self.h) or not (0 <= c < self.w) or self.tiles[r][c].flipped or (r, c) in self.mines:
      return
    # Flip tile
    if self.tiles[r][c].flagged:
      self.tiles[r][c].trigger_flag()
    self.tiles[r][c].flip_self()
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
      if self.tiles[r][c].flagged:
        self.flag_count += 1
      else:
        self.flag_count -= 1
      self.tiles[r][c].trigger_flag()

