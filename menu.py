import config
import pygame as pg

class Menu:
    def __init__(self, window):
        self.window = window
        self.grid_size = 3
        self.starting_player = 'X'
        self.start_game = False

    def render_menu(self):
        self.start_game = True
