from src import config
from src.tile import Tile
import pygame as pg
import os

class Menu:
    TITLE_SCALE_FACTOR = 0.40
    START_BUTTON_SCALE_FACTOR = 0.125

    def __init__(self, window):
        self.window = window
        self.grid_size = 3
        self.starting_player = 'X'
        self.start_game = False

        self.title_img = pg.image.load(os.path.join('Assets', 'tictactoe.png'))
        self.title = pg.transform.scale(self.title_img, (self.title_img.get_width() * Menu.TITLE_SCALE_FACTOR,\
                                                        self.title_img.get_height() * Menu.TITLE_SCALE_FACTOR))
        self.title_rect = self.title.get_rect()
        self.title_rect.center = (config.WINDOW_WIDTH // 2, 100)

        self.start_img = pg.image.load(os.path.join('Assets', 'start.png'))
        self.start_button = pg.transform.scale(self.start_img, (self.start_img.get_width() * Menu.START_BUTTON_SCALE_FACTOR,\
                                                                self.start_img.get_height() * Menu.START_BUTTON_SCALE_FACTOR))
        self.start_button_rect = self.start_button.get_rect()
        self.start_button_rect.center = (config.WINDOW_WIDTH // 2, 600)

    def draw_menu(self):
        self.window.blit(self.title, self.title_rect)
        self.window.blit(self.start_button, self.start_button_rect)

    def click(self, mouse_pos):
        x, y = mouse_pos
        if self.start_button_rect.collidepoint(x, y):
            self.start_game = True
