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

    def click(self, mouse_pos, player):
        # check if mouse is on tiles
        if 0 <= mouse_pos[0] <= config.WINDOW_WIDTH and 0 <= mouse_pos[1] <= config.WINDOW_WIDTH: 
            col = mouse_pos[0] // self.tile_size
            row = mouse_pos[1] // self.tile_size
            tile_idx = self.grid_size * row + col
            if self.tiles[tile_idx].update_marking(player):
                return 'O' if player == 'X' else 'X'
            
        return player