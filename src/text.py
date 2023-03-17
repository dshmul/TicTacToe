import pygame as pg

class Text:
    def __init__(self, text, font, color, center_x, center_y):
        self.text = font.render(text, True, color)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (center_x, center_y)

        self.font = font
        self.color = color

    def draw(self, window):
        window.blit(self.text, self.text_rect)

    def update_text(self, text):
        self.text = self.font.render(text, True, self.color)