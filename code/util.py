import pygame, os

def load_image(fn, scale = 1):
  image = pygame.image.load(os.path.join('assets', 'images', fn + '.png')).convert_alpha()
  image = pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))
  return image

def load_font(fn, size = 32):
  font = pygame.font.Font(os.path.join('assets', 'fonts', fn + '.ttf'), size)
  return font

def draw_text(surface, font, text, color, x, y):
    text = font.render(text, False, color)
    text_rect = text.get_rect(center = (x, y))
    surface.blit(text, text_rect)