from src import config
from src.menu import Menu
from src.board import Board
from src.scoreboard import Scoreboard
import pygame as pg
import sys
import requests

class Game:
    MAX_INPUT_LENGTH = 10

    def __init__(self):
        pg.init()
        self.window = pg.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        pg.display.set_caption(config.TITLE)
        self.window_state = "menu" 
        self.menu = Menu(self.window)
        self.current_player = self.menu.player1
        self.board = Board(self.window, self.menu)
        self.scoreboard = Scoreboard(self.window, self.menu)
        self.board.init_tiles()
        self.running = True
        self.pause_grid = False
        self.game_state = ""
        self.active_input = None
        self.counter = False
        self.delay_count = 0

    def run(self):
        '''Game runnning loop'''
        clock = pg.time.Clock()
        while self.running:
            clock.tick(config.FPS)
            self.events()
            self.render()
        
    def events(self):
        '''Event handler'''
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.window_state == "menu" and self.menu.api_connection:
                    self.window_state = self.menu.click(pg.mouse.get_pos())

                    if self.window_state == "board":
                        self.scoreboard.update_player_names()
                    elif self.window_state == "update_board":
                            self.board.init_tiles()
                            self.pause_grid = False
                            self.game_state = ""
                            self.window_state = "menu"

                    if self.game_state == "expired" and self.menu.player1.logged_in and self.menu.player2.logged_in:
                            self.board.init_tiles()
                            self.pause_grid = False
                            self.game_state = ""

                elif self.window_state == "board":
                    if pg.mouse.get_pos()[1] <= config.WINDOW_WIDTH:
                        if not self.pause_grid and self.game_state != "expired":
                            self.window_state, valid_press = self.board.grid_click(pg.mouse.get_pos(), self.current_player)
                            if valid_press:
                                self.update_game_state()

                        if self.game_state:
                            self.window_state, reset_board = self.board.popup_click(pg.mouse.get_pos(), self.game_state)

                            if reset_board:
                                self.board.init_tiles()
                                self.pause_grid = False
                                self.game_state = ""

                    else:
                        self.window_state = self.board.options_click(pg.mouse.get_pos())
                        if self.window_state == "switch_player":
                            self.current_player = self.menu.player2 if self.current_player.marker == "X" else self.menu.player1
                            self.window_state = "board"
                    
                elif self.window_state == "score":
                    self.window_state = self.scoreboard.click(pg.mouse.get_pos())

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE:
                    self.menu.active_input.input = self.menu.active_input.input[:-1]
                elif self.menu.active_input and len(self.menu.active_input.input) <= Game.MAX_INPUT_LENGTH \
                        and event.key != pg.K_TAB and event.key != pg.K_BACKSLASH:
                    self.menu.active_input.input += event.unicode

            if event.type == pg.QUIT:
                self.quit()
            
    def render(self):
        '''Render window depending on game state'''
        self.window.fill(config.WHITE)

        if self.window_state == "menu":
            self.menu.draw_menu()

        elif self.window_state == "board":
            self.board.draw_board(self.current_player)
            
            if not self.menu.player1.validate_token() or not self.menu.player2.validate_token():
                self.game_state = "expired"

            if self.game_state:
                self.board.draw_popup(self.game_state, self.current_player)
                self.board.freeze_restart = True
            else:
                self.board.freeze_restart = False

        elif self.window_state == "score":
            self.scoreboard.draw_scoreboard(self.menu.grid_size)

        pg.display.update()

    def update_game_state(self):
        if self.board.check_win():
            reply = requests.post(config.API_ADDR + "score",\
                                 json={"score": 1 + self.board.open_tile_count, "grid_size": self.menu.grid_size},\
                                    headers={"x-access-token": self.current_player.token}).json()
            self.pause_grid = True
            self.game_state = "win"
            print(f"{reply['message']} | Player {self.current_player.marker!r} WON - SCORE: {1 + self.board.open_tile_count}")
        elif self.board.check_draw():
            self.pause_grid = True
            self.game_state = "draw"
            print("DRAW")
        else:
            self.current_player = self.menu.player2 if self.current_player.marker == "X" else self.menu.player1

    def quit(self):
        '''Terminate the program'''
        pg.quit()
        sys.exit()