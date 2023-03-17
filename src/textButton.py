import pygame as pg
from src import config

class TextButton:
    def __init__(self, text, text_font, text_color, rect_color, width, height, center_x, center_y, border_radius=-1, border_outline=False):
        self.button_rect = pg.Rect((0, 0), (width, height))
        self.button_rect.center = (center_x, center_y)

        self.text = text_font.render(text, True, text_color)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.button_rect.center

        self.text_font = text_font
        self.text_color = text_color
        self.rect_color = rect_color
        self.border_radius = border_radius
        self.border_outline = border_outline

    def draw(self, window, color=None):
        pg.draw.rect(window, color if color else self.rect_color, self.button_rect, self.border_radius, 5, 5, 5, 5)
        if self.border_outline:
            pg.draw.rect(window, config.BLACK, self.button_rect, 1, 5, 5, 5, 5)
        window.blit(self.text, self.text_rect)
    
    def update_text(self, text):
        self.text = self.text_font.render(text, True, self.text_color)
