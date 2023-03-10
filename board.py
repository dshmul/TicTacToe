import config
from tile import Tile
import pygame as pg
import numpy as np

class Board:
    def __init__(self, window, grid_size):
        self.window = window
        self.grid_size = grid_size
        self.tiles = []
        self.tile_size = config.WINDOW_WIDTH // grid_size

    def init_tiles(self):
        Tile.tile_size = self.tile_size

        for r in range(self.grid_size):
            for c in range(self.grid_size):
                self.tiles.append(Tile(r, c))

    def draw_board(self):
        for tile in self.tiles:
            tile.draw(self.window)

       