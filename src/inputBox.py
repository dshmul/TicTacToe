from src import config
import pygame as pg

class InputBox():
    def __init__(self, center_x, center_y, width, height, initial_text):
        self.entry_rect = pg.Rect((0, 0), (width, height))
        self.entry_rect.center = (center_x, center_y) 

        self.initial_text = config.TEXT_FONT.render(initial_text, True, config.LIGHT_GRAY)
        self.initial_text_rect = self.initial_text.get_rect()
        self.initial_text_rect.center = self.entry_rect.center

        self.active = False
        self.invalid = False
        self.input = ""

    def draw(self, window):
        if self.active:
            if self.invalid:
                pg.draw.rect(window, config.DARK_RED, self.entry_rect, 3, 5, 5, 5, 5)
            else:
                pg.draw.rect(window, config.ORANGE, self.entry_rect, 3, 5, 5, 5, 5)
        elif self.invalid:
            pg.draw.rect(window, config.RED, self.entry_rect, 3, 5, 5, 5, 5)
        else:
            pg.draw.rect(window, config.LIGHT_ORANGE, self.entry_rect, 3, 5, 5, 5, 5)

        if self.input == "":
            window.blit(self.initial_text, self.initial_text_rect)
        else:
            text = config.TEXT_FONT.render(self.input, True, config.BLACK)
            text_rect = text.get_rect()
            text_rect.center = self.entry_rect.center
            window.blit(text, text_rect)

