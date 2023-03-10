import config
from tile import Tile
import pygame as pg
import os

class Menu:
    def __init__(self, window):
        self.window = window
        self.grid_size = 3
        self.starting_player = 'X'
        self.start_game = False

    def draw_menu(self):
        self.start_game = True
