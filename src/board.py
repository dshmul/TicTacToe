from src import config
from src.tile import Tile
from src.playerIndicator import PlayerIndicator
from src.imageButton import ImageButton
from src.textButton import TextButton
from src.text import Text
import pygame as pg
import numpy as np
import os

class Board:
    MENU_BUTTON_SCALE_FACTOR = .075
    RESTART_BUTTON_SCALE_FACTOR = .25
    START_BUTTON_SCALE_FACTOR = .125
    NEW_GAME_BUTTON_SCALE_FACTOR = 0.4
    WINNING_MARKER_SIZE = 100

    def __init__(self, window, menu):
        self.window = window
        self.menu = menu
        self.tiles = []
        self.open_tile_count = 0
        self.freeze_restart = False
        Tile.tile_size = config.WINDOW_WIDTH // self.menu.grid_size

        self.popup = pg.Rect((0, 0), (383, 383))
        self.popup.center = (config.WINDOW_WIDTH // 2, config.WINDOW_WIDTH // 2)

        self.menu_img = pg.image.load(os.path.join('assets', 'menu.png'))
        self.menu_button = ImageButton(self.menu_img, self.menu_img.get_width() * Board.MENU_BUTTON_SCALE_FACTOR, \
                                       self.menu_img.get_height() * Board.MENU_BUTTON_SCALE_FACTOR, 40, 650)

        self.restart_img = pg.image.load(os.path.join('assets', 'restart.png'))
        self.restart_button = ImageButton(self.restart_img, self.restart_img.get_width() * Board.RESTART_BUTTON_SCALE_FACTOR, \
                                          self.restart_img.get_height() * Board.RESTART_BUTTON_SCALE_FACTOR, 100, 650)
        
        self.podium_img = pg.image.load(os.path.join('assets', 'podium.png'))
        self.podium_button = ImageButton(self.podium_img, 80, 80, 550, 650)

        # Surfacs for popup
        self.new_game_button = TextButton("Start New Game", config.HEADER_FONT, config.BLACK, config.YELLOW, \
                                          200, 50, config.WINDOW_WIDTH // 2, 415, 25, True)
        
        self.expired_token_msg = Text("User session expired...", config.HEADER_FONT, config.RED, \
                                      config.WINDOW_WIDTH // 2, config.WINDOW_WIDTH // 2)
        
        self.popup_menu_button = TextButton("Return to Menu", config.HEADER_FONT, config.BLACK, config.RED, \
                                            200, 50, config.WINDOW_WIDTH // 2, 415, 25, True)
        
        self.x_img = pg.image.load(os.path.join('assets', 'x.png'))
        self.x_marker = ImageButton(self.x_img, Board.WINNING_MARKER_SIZE, Board.WINNING_MARKER_SIZE, \
                                    config.WINDOW_WIDTH // 2, config.WINDOW_WIDTH // 2)

        self.o_img = pg.image.load(os.path.join('assets', 'o.png'))
        self.o_marker = ImageButton(self.o_img, Board.WINNING_MARKER_SIZE, Board.WINNING_MARKER_SIZE, \
                                    config.WINDOW_WIDTH // 2, config.WINDOW_WIDTH // 2)

    def init_tiles(self):
        Tile.tile_size = config.WINDOW_WIDTH // self.menu.grid_size
        self.tiles.clear()
        self.open_tile_count = self.menu.grid_size ** 2

        for r in range(self.menu.grid_size):
            for c in range(self.menu.grid_size):
                self.tiles.append(Tile(r, c))

    def draw_board(self, current_player):
        for tile in self.tiles:
            tile.draw(self.window)

        self.menu_button.draw(self.window)
        self.restart_button.draw(self.window)
        self.podium_button.draw(self.window)

        # Surface for current player
        self.player1_indicator = PlayerIndicator(self.menu.player1, False, config.WINDOW_WIDTH // 2 - 70, 650)
        self.player2_indicator = PlayerIndicator(self.menu.player2, False, config.WINDOW_WIDTH // 2 + 110, 650)
        self.player1_active_indicator = PlayerIndicator(self.menu.player1, True, config.WINDOW_WIDTH // 2 - 70, 650)
        self.player2_active_indicator = PlayerIndicator(self.menu.player2, True, config.WINDOW_WIDTH // 2 + 110, 650)

        if current_player.marker == "X":
            self.player1_active_indicator.draw(self.window)
            self.player2_indicator.draw(self.window)
        elif current_player.marker == "O":
            self.player1_indicator.draw(self.window)
            self.player2_active_indicator.draw(self.window)
       
    def draw_popup(self, game_state, current_player): 
        pg.draw.rect(self.window, config.GRAY, self.popup, 200, 50, 50, 50, 50)

        if game_state == "win":
            winner_msg = Text(f"{current_player.username} WON!", config.TITLE_FONT, config.BLACK, config.WINDOW_WIDTH // 2, 175)
            winner_msg.draw(self.window)

            score_msg = Text(f"Score: {1 + self.open_tile_count}", config.HEADER_FONT, config.BLACK, config.WINDOW_WIDTH // 2, 210)
            score_msg.draw(self.window)

            if current_player.marker == 'X':
                self.x_marker.update_center(config.WINDOW_WIDTH // 2, config.WINDOW_WIDTH // 2)
                self.x_marker.draw(self.window)
            elif current_player.marker == 'O':
                self.o_marker.update_center(config.WINDOW_WIDTH // 2, config.WINDOW_WIDTH // 2)
                self.o_marker.draw(self.window)

        elif game_state == "draw":
            draw_msg = Text(f"DRAW :\\", config.EXTRA_BIG_FONT, config.BLACK, config.WINDOW_WIDTH // 2, 200)
            draw_msg.draw(self.window)

            self.x_marker.update_center(config.WINDOW_WIDTH // 2 - 70, config.WINDOW_WIDTH // 2)
            self.x_marker.draw(self.window)
            self.o_marker.update_center(config.WINDOW_WIDTH // 2 + 70, config.WINDOW_WIDTH // 2)
            self.o_marker.draw(self.window)

        if game_state != "expired":
            self.new_game_button.draw(self.window)
        else:
            self.expired_token_msg.draw(self.window)
            self.popup_menu_button.draw(self.window)

    def grid_click(self, mouse_pos, current_player):
        col = mouse_pos[0] // Tile.tile_size
        row = mouse_pos[1] // Tile.tile_size
        tile_idx = self.menu.grid_size * row + col

        valid_press = self.tiles[tile_idx].update_marking(current_player.marker)
        if valid_press:
            self.open_tile_count -= 1
                
        return "board", valid_press
    
    def popup_click(self, mouse_pos, game_state):
        x, y = mouse_pos
        if self.new_game_button.button_rect.collidepoint(x, y) and game_state != "expired":
            return "board", True
        elif self.popup_menu_button.button_rect.collidepoint(x, y):
            return "menu", False
        
        return "board", False
            
    def options_click(self, mouse_pos):
        x, y = mouse_pos
        if self.menu_button.button_rect.collidepoint(x, y):
            return "menu"
        elif self.restart_button.button_rect.collidepoint(x, y) and not self.freeze_restart: 
            self.init_tiles()
        elif (self.player1_indicator.bounding_rect.collidepoint(x, y) or self.player2_indicator.bounding_rect.collidepoint(x, y))\
                and self.open_tile_count == self.menu.grid_size ** 2:
            return "switch_player"
        elif self.podium_button.button_rect.collidepoint(x, y):
            return "score"
        return "board"
    
    def check_draw(self):
        return True if self.open_tile_count <= 0 else False
    
    def check_win(self):
        tiles_reshaped = np.reshape(self.tiles, (self.menu.grid_size, self.menu.grid_size))

        for i in range(self.menu.grid_size):
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