import pygame
from random import randint
from states.state import State
from states.board import Board
from settings import *
from util import *

class Title(State):
  def __init__(self, game):
    super().__init__(game)
    self.title_font = load_font('LycheeSoda', 64)
    self.font = load_font('LycheeSoda')
    self.font_color = 'White'
    self.font_hover = (255, 62, 139)

    self.tiles = [[] for i in range(BOARD_HEIGHT + UI_HEIGHT)]

    for r in range(0, BOARD_HEIGHT + UI_HEIGHT):
      for c in range(0, BOARD_WIDTH):
        tile_surface = load_image('grass_' + str(randint(1,4)), IMAGE_SCALE)
        self.tiles[r].append(tile_surface)

    self.difficulty_button_text = ['<','>']
    self.difficulty_buttons_rect = []
    self.difficulty_buttons_methods = [self.prev_difficulty, self.next_difficulty]

    for i in range(len(self.difficulty_button_text)): 
      weirdmath = (i - 1) * 64 + (i * 64)
      text = self.font.render(self.difficulty_button_text[i], False, self.font_color)
      text_rect = text.get_rect(center = (SCREEN_WIDTH//2 + weirdmath, SCREEN_HEIGHT//3 + 40))
      self.difficulty_buttons_rect.append(text_rect)

    self.difficulties = list(DIFFICULTIES.keys())
    self.d_index = self.difficulties.index(self.game.difficulty)

    self.menu_text = ['Start', 'Quit']
    self.menu_rect = []
    self.menu_screen = [self.start, self.quit]

    for i in range(len(self.menu_text)):  
      text = self.font.render(self.menu_text[i], False, self.font_color)
      text_rect = text.get_rect(center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//3 + 100 + 40 * i))

      self.menu_rect.append(text_rect)

  def prev_difficulty(self):
    if self.d_index > 0:
      self.d_index -= 1
    else:
      self.d_index = len(self.difficulties) - 1
    self.game.difficulty = self.difficulties[self.d_index]

  def next_difficulty(self):
    if self.d_index < len(self.difficulties) - 1:
      self.d_index += 1
    else:
      self.d_index = 0
    self.game.difficulty = self.difficulties[self.d_index]

  def start(self):
    new_state = Board(self.game)
    new_state.enter_state()
    self.game.reset_keys()

  def quit(self):
    self.game.running = False

  def update(self, actions):
    if actions['lmb'] and pygame.time.get_ticks() - self.game.click_icd > 200:
      self.game.click_icd = pygame.time.get_ticks()
      for i in range(len(self.menu_rect)):
        if self.menu_rect[i].collidepoint(pygame.mouse.get_pos()):
          self.menu_screen[i]()
          return
      for i in range(len(self.difficulty_buttons_rect)):
        if self.difficulty_buttons_rect[i].collidepoint(pygame.mouse.get_pos()):
          self.difficulty_buttons_methods[i]()
          return

  def render(self, display):
    for r in range(0, BOARD_HEIGHT + UI_HEIGHT):
      for c in range(0, BOARD_WIDTH):
        tile_rect = self.tiles[r][c].get_rect(topleft = (c * TILE_SIZE, r * TILE_SIZE))
        display.blit(self.tiles[r][c], tile_rect)
      
    draw_text(display, self.title_font, 'Minesweeper', self.font_color, SCREEN_WIDTH//2, SCREEN_HEIGHT//3)
    for i in range(len(self.difficulty_buttons_rect)):
      x, y = self.difficulty_buttons_rect[i].center
      if self.difficulty_buttons_rect[i].collidepoint(pygame.mouse.get_pos()):
        draw_text(display, self.font, self.difficulty_button_text[i], self.font_hover, x, y)
      else:
        draw_text(display, self.font, self.difficulty_button_text[i], self.font_color, x, y)
    draw_text(display, self.font, self.game.difficulty, self.font_color, SCREEN_WIDTH//2, SCREEN_HEIGHT//3 + 40)

    for i in range(len(self.menu_text)):
      x, y = self.menu_rect[i].center
      if self.menu_rect[i].collidepoint(pygame.mouse.get_pos()):
        draw_text(display, self.font, self.menu_text[i], self.font_hover, x, y)
      else:
        draw_text(display, self.font, self.menu_text[i], self.font_color, x, y)
