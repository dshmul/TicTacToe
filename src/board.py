from src import config
from src.tile import Tile
import pygame as pg
import numpy as np
import os

class Board:
    MENU_BUTTON_SCALE_FACTOR = .075
    RESTART_BUTTON_SCALE_FACTOR = .25
    START_BUTTON_SCALE_FACTOR = .125

    def __init__(self, window, grid_size):
        self.window = window
        self.grid_size = grid_size
        self.tiles = []
        self.open_tile_count = 0
        Tile.tile_size = config.WINDOW_WIDTH // grid_size

        self.font = pg.font.Font(pg.font.get_default_font(), config.TEXT_SIZE)
        self.popup = pg.Rect((0, 0), (400, 400))
        self.popup.center = (config.WINDOW_WIDTH // 2, config.WINDOW_WIDTH // 2)

        self.menu_img = pg.image.load(os.path.join('Assets', 'menu.png'))
        self.menu_button = pg.transform.scale(self.menu_img, (self.menu_img.get_width() * Board.MENU_BUTTON_SCALE_FACTOR,\
                                                              self.menu_img.get_height() * Board.MENU_BUTTON_SCALE_FACTOR))
        self.menu_button_rect = self.menu_button.get_rect()
        self.menu_button_rect.center = (40, 650)

        self.restart_img = pg.image.load(os.path.join('Assets', 'restart.png'))
        self.restart_button = pg.transform.scale(self.restart_img, (self.restart_img.get_width() * Board.RESTART_BUTTON_SCALE_FACTOR,\
                                                                  self.restart_img.get_height() * Board.RESTART_BUTTON_SCALE_FACTOR))
        self.restart_button_rect = self.restart_button.get_rect()
        self.restart_button_rect.center = (100, 650)

        self.podium_img = pg.image.load(os.path.join('Assets', 'podium.png'))
        self.podium_button = pg.transform.scale(self.podium_img, (80, 80))
        self.podium_button_rect = self.podium_button.get_rect()
        self.podium_button_rect.center = (550, 650)

        self.start_img = pg.image.load(os.path.join('Assets', 'start.png'))
        self.start_button = pg.transform.scale(self.start_img, (self.start_img.get_width() * Board.START_BUTTON_SCALE_FACTOR,\
                                                                self.start_img.get_height() * Board.START_BUTTON_SCALE_FACTOR))
        self.start_button_rect = self.start_button.get_rect()
        self.start_button_rect.center = (config.WINDOW_WIDTH // 2, 400)

    def init_tiles(self):
        self.tiles.clear()
        self.open_tile_count = self.grid_size ** 2

        for r in range(self.grid_size):
            for c in range(self.grid_size):
                self.tiles.append(Tile(r, c))

    def draw_board(self):
        for tile in self.tiles:
            tile.draw(self.window)

        self.window.blit(self.menu_button, self.menu_button_rect)
        self.window.blit(self.restart_button, self.restart_button_rect)
        self.window.blit(self.podium_button, self.podium_button_rect)

    def draw_popup(self, text):
        text = self.font.render(text, True, config.BLACK)
        text_rect = text.get_rect()
        text_rect.center = self.popup.center
        pg.draw.rect(self.window, config.GRAY, self.popup, 200, 50, 50, 50, 50)
        self.window.blit(text, text_rect)

        self.window.blit(self.start_button, self.start_button_rect)
        
    def grid_click(self, mouse_pos, player):
        # check if click is on tiles
        if 0 <= mouse_pos[0] < config.WINDOW_WIDTH and 0 <= mouse_pos[1] < config.WINDOW_WIDTH: 
            col = mouse_pos[0] // Tile.tile_size
            row = mouse_pos[1] // Tile.tile_size
            tile_idx = self.grid_size * row + col
            if self.tiles[tile_idx].update_marking(player):
                self.open_tile_count -= 1
                
        return "board"
    
    def popup_click(self, mouse_pos):
        x, y = mouse_pos
        if self.start_button_rect.collidepoint(x, y):
            return True
        return False
            
    def options_click(self, mouse_pos):
        x, y = mouse_pos
        if self.menu_button_rect.collidepoint(x, y):
            return "menu"
        elif self.restart_button_rect.collidepoint(x, y): #TODO: make sure logical
            self.init_tiles()
        elif self.podium_button_rect.collidepoint(x, y):
            return "score"
        return "board"
    
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