from src import config
import pygame as pg
import os

class PlayerIndicator:
    MARKER_SIZE = 50

    def __init__(self, user, active, center_x, center_y):
        self.marker = user.marker
        self.username = user.username
        self.active = active

        self.bounding_rect = pg.Rect((0, 0), (160, 75))
        self.bounding_rect.center = (center_x, center_y) 

        if self.marker == "X":
            self.marker = pg.image.load(os.path.join('s', 'x.png'))
        elif self.marker == "O":
            self.marker = pg.image.load(os.path.join('assets', 'o.png'))
    
        self.marker = pg.transform.scale(self.marker, (PlayerIndicator.MARKER_SIZE, PlayerIndicator.MARKER_SIZE))
        self.marker_rect = self.marker.get_rect()
        self.marker_rect.center = (center_x - 45, center_y)

        self.username_text = config.TEXT_FONT.render(self.username, True, config.BLACK)
        self.username_text_rect = self.username_text.get_rect()
        self.username_text_rect.center = (center_x + 20, center_y)

    def draw(self, window):
        if self.active:
            pg.draw.rect(window, config.LIGHT_GREEN, self.bounding_rect)
            pg.draw.rect(window, config.BLACK, self.bounding_rect, 3, 0, 0, 0, 0)

        else:
            pg.draw.rect(window, config.BLACK, self.bounding_rect, 3, 0, 0, 0, 0)

        window.blit(self.marker, self.marker_rect)
        window.blit(self.username_text, self.username_text_rect)

