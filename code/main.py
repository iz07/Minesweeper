import pygame

from settings import *
from util import *
from board import Board

class Game:
  def __init__(self) -> None:
    pygame.init()
    pygame.display.set_caption('Minesweeper')
    self.running = True
    self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    self.clock = pygame.time.Clock()
    self.font = load_font('LycheeSoda')
    self.last_click = 0

    self.setup()

  def setup(self):
    self.playing = True
    self.start_game = False
    self.board = Board()

  def get_events(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.running = False
      # left click for dig
      if self.playing and pygame.mouse.get_pressed()[0] and pygame.time.get_ticks() - self.last_click > 150:
        self.last_click = pygame.time.get_ticks()
        pos = pygame.mouse.get_pos()
        c, r = pos[0] // TILE_SIZE, pos[1] // TILE_SIZE
        # This is the first click, create board around this point
        if not self.start_game:
          self.start_game = True
          self.board.load_data((r, c))
        if self.board.tiles[r][c].flagged:
          pass
        elif self.board.tiles[r][c].mines_nearby == -1:
          self.board.clear_flags()
          self.board.flip_mines()
          self.playing = False
        else: self.board.flip_tile(r, c)
      # right click for flags
      if self.playing and pygame.mouse.get_pressed()[2] and pygame.time.get_ticks() - self.last_click > 150:
        self.last_click = pygame.time.get_ticks()
        pos = pygame.mouse.get_pos()
        c, r = pos[0] // TILE_SIZE, pos[1] // TILE_SIZE
        self.board.flag_tile(r, c)
      if event.type == pygame.KEYDOWN:
        if not self.playing and event.key == pygame.K_SPACE:
          self.setup()

  def run(self):
    while self.running:
      self.get_events()
      
      if self.board.render(self.screen):
        self.playing = False
        draw_text(self.screen, self.font, 'You win!', 'White', SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        draw_text(self.screen, self.font, 'Press space to play again', 'White', SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 48)
      elif not self.playing:
        draw_text(self.screen, self.font, 'You lose', 'White', SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        draw_text(self.screen, self.font, 'Press space to play again', 'White', SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 48)


      pygame.display.update()
      self.clock.tick(60)

if __name__ == '__main__':
  Game().run()