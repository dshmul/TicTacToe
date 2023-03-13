import config
from tile import Tile
import pygame as pg
import numpy as np
import os

class Board:
    def __init__(self, window, grid_size):
        self.window = window
        self.grid_size = grid_size
        self.tiles = []
        self.open_tile_count = 0
        Tile.tile_size = config.WINDOW_WIDTH // grid_size

    def init_tiles(self):
        self.tiles.clear()
        self.open_tile_count = self.grid_size ** 2

        for r in range(self.grid_size):
            for c in range(self.grid_size):
                self.tiles.append(Tile(r, c))

    def draw_board(self):
        for tile in self.tiles:
            tile.draw(self.window)

        # TODO: remove hardcoding
        podium_img = pg.image.load(os.path.join('Assets', 'podium.png'))
        podium_img = pg.transform.scale(podium_img, (80, 80))
        self.window.blit(podium_img, (510, 610))

    def click(self, mouse_pos, player):
        # check if click is on tiles
        if 0 <= mouse_pos[0] <= config.WINDOW_WIDTH and 0 <= mouse_pos[1] <= config.WINDOW_WIDTH: 
            col = mouse_pos[0] // Tile.tile_size
            row = mouse_pos[1] // Tile.tile_size
            tile_idx = self.grid_size * row + col
            if self.tiles[tile_idx].update_marking(player):
                self.open_tile_count -= 1
                return 'O' if player == 'X' else 'X', "board"
            
        # TODO: remove hardcoding
        # scoreboard button
        elif 510 <= mouse_pos[0] <= 590 and 610 <= mouse_pos[1] <= 690:
            return player, "score"

        return player, "board"
    
    def check_draw(self):
        return True if self.open_tile_count <= 0 else False
    
    def check_win(self):
        tiles_reshaped = np.reshape(self.tiles, (self.grid_size, self.grid_size))

        for i in range(self.grid_size):
            # check row
            if all(tile.marking and tile.marking == tiles_reshaped[i, 0].marking for tile in tiles_reshaped[i, :]):
                return True

            # check column
            if all(tile.marking and tile.marking == tiles_reshaped[0, i].marking for tile in tiles_reshaped[:, i]):
                return True
        
        # check main diagonal
        if all(tile.marking and tile.marking == tiles_reshaped[0, 0].marking for tile in tiles_reshaped.diagonal()):
            return True
        
        # check reverse diagonal
        if all(tile.marking and tile.marking == tiles_reshaped[-1, 0].marking for tile in np.flipud(tiles_reshaped).diagonal()):
            return True

        return False