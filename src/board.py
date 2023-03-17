from src import config
from src.tile import Tile
from src.playerIndicator import PlayerIndicator
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
        self.menu_button = pg.transform.scale(self.menu_img, (self.menu_img.get_width() * Board.MENU_BUTTON_SCALE_FACTOR,\
                                                              self.menu_img.get_height() * Board.MENU_BUTTON_SCALE_FACTOR))
        self.menu_button_rect = self.menu_button.get_rect()
        self.menu_button_rect.center = (40, 650)

        self.restart_img = pg.image.load(os.path.join('assets', 'restart.png'))
        self.restart_button = pg.transform.scale(self.restart_img, (self.restart_img.get_width() * Board.RESTART_BUTTON_SCALE_FACTOR,\
                                                                  self.restart_img.get_height() * Board.RESTART_BUTTON_SCALE_FACTOR))
        self.restart_button_rect = self.restart_button.get_rect()
        self.restart_button_rect.center = (100, 650)

        self.podium_img = pg.image.load(os.path.join('assets', 'podium.png'))
        self.podium_button = pg.transform.scale(self.podium_img, (80, 80))
        self.podium_button_rect = self.podium_button.get_rect()
        self.podium_button_rect.center = (550, 650)

        # Surfacs for popup
        self.new_game_button_rect = pg.Rect((0, 0), (200, 50))
        self.new_game_button_rect.center = (config.WINDOW_WIDTH // 2, 415)

        self.new_game_text = config.HEADER_FONT.render("Start New Game", True, config.BLACK)
        self.new_game_text_rect = self.new_game_text.get_rect()
        self.new_game_text_rect.center = self.new_game_button_rect.center

        self.expired_token_msg = config.HEADER_FONT.render("User session expired...", True, config.RED)
        self.expired_token_msg_rect = self.expired_token_msg.get_rect()
        self.expired_token_msg_rect.center = (config.WINDOW_WIDTH // 2, config.WINDOW_WIDTH // 2)

        self.menu_popup_button_rect = pg.Rect((0, 0), (200, 50))
        self.menu_popup_button_rect.center = (config.WINDOW_WIDTH // 2, 415)

        self.menu_text = config.HEADER_FONT.render("Return to Menu", True, config.BLACK)
        self.menu_text_rect = self.menu_text.get_rect()
        self.menu_text_rect.center = self.menu_popup_button_rect.center

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

        self.window.blit(self.menu_button, self.menu_button_rect)
        self.window.blit(self.restart_button, self.restart_button_rect)
        self.window.blit(self.podium_button, self.podium_button_rect)

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
            winner_msg = config.TITLE_FONT.render(f"{current_player.username} WON!", True, config.BLACK)
            winner_msg_rect = winner_msg.get_rect()
            winner_msg_rect.center = (config.WINDOW_WIDTH // 2, 175)
            self.window.blit(winner_msg, winner_msg_rect)

            score_msg = config.HEADER_FONT.render(f"Score: {1 + self.open_tile_count}", True, config.BLACK) 
            score_msg_rect = score_msg.get_rect()
            score_msg_rect.center = (config.WINDOW_WIDTH // 2, 210)
            self.window.blit(score_msg, score_msg_rect)

            if current_player.marker == 'X':
                marker_img = pg.image.load(os.path.join('assets', 'x.png'))
            elif current_player.marker == 'O':
                marker_img = pg.image.load(os.path.join('assets', 'o.png'))

            marker = pg.transform.scale(marker_img, (Board.WINNING_MARKER_SIZE,\
                                                    Board.WINNING_MARKER_SIZE))
            marker_rect = marker.get_rect()
            marker_rect.center = (config.WINDOW_WIDTH // 2, config.WINDOW_WIDTH // 2)
            self.window.blit(marker, marker_rect)
        elif game_state == "draw":
            draw_msg = config.EXTRA_BIG_FONT.render(f"DRAW :\\", True, config.BLACK)
            draw_msg_rect = draw_msg.get_rect()
            draw_msg_rect.center = (config.WINDOW_WIDTH // 2, 200)
            self.window.blit(draw_msg, draw_msg_rect)

            x_marker_img = pg.image.load(os.path.join('assets', 'x.png'))
            x_marker = pg.transform.scale(x_marker_img, (Board.WINNING_MARKER_SIZE,\
                                                    Board.WINNING_MARKER_SIZE))
            x_marker_rect = x_marker.get_rect()
            x_marker_rect.center = (config.WINDOW_WIDTH // 2 - 70, config.WINDOW_WIDTH // 2)
            self.window.blit(x_marker, x_marker_rect)

            o_marker_img = pg.image.load(os.path.join('assets', 'o.png'))
            o_marker = pg.transform.scale(o_marker_img, (Board.WINNING_MARKER_SIZE,\
                                                    Board.WINNING_MARKER_SIZE))
            o_marker_rect = o_marker.get_rect()
            o_marker_rect.center = (config.WINDOW_WIDTH // 2 + 70, config.WINDOW_WIDTH // 2)
            self.window.blit(o_marker, o_marker_rect)

        if game_state != "expired":
            pg.draw.rect(self.window, config.YELLOW, self.new_game_button_rect, 25, 5, 5, 5, 5)
            self.window.blit(self.new_game_text, self.new_game_text_rect)
        else:
            self.window.blit(self.expired_token_msg, self.expired_token_msg_rect)

            pg.draw.rect(self.window, config.RED, self.menu_popup_button_rect, 25, 5, 5, 5, 5)
            self.window.blit(self.menu_text, self.menu_text_rect)

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
        if self.new_game_button_rect.collidepoint(x, y) and game_state != "expired":
            return "board", True
        elif self.menu_popup_button_rect.collidepoint(x, y):
            return "menu", False
        
        return "board", False
            
    def options_click(self, mouse_pos):
        x, y = mouse_pos
        if self.menu_button_rect.collidepoint(x, y):
            return "menu"
        elif self.restart_button_rect.collidepoint(x, y) and not self.freeze_restart: 
            self.init_tiles()
        elif (self.player1_indicator.bounding_rect.collidepoint(x, y) or self.player2_indicator.bounding_rect.collidepoint(x, y))\
                and self.open_tile_count == self.menu.grid_size ** 2:
            return "switch_player"
        elif self.podium_button_rect.collidepoint(x, y):
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