from src import config
from src.menu import Menu
from src.board import Board
from src.scoreboard import Scoreboard
import pygame as pg
import sys
from threading import Thread

class Game:
    def __init__(self):
        pg.init()
        self.window = pg.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        pg.display.set_caption(config.TITLE)
        self.window_state = "menu" 
        self.menu = Menu(self.window)
        self.current_player = self.menu.starting_player
        self.board = Board(self.window, self.menu)
        self.scoreboard = Scoreboard(self.window)
        self.board.init_tiles()
        self.running = True
        self.pause_grid = False
        self.game_state = ""
        self.active_input = None

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
                    
                    if self.window_state == "update_board":
                            self.board.init_tiles()
                            self.window_state = "menu"

                elif self.window_state == "board":
                    if pg.mouse.get_pos()[1] <= config.WINDOW_WIDTH:
                        if not self.pause_grid:
                            self.window_state, valid_press = self.board.grid_click(pg.mouse.get_pos(), self.current_player)
                            if valid_press:
                                self.update_game_state()
                        elif self.board.popup_click(pg.mouse.get_pos()):
                            self.board.init_tiles()
                            self.pause_grid = False
                            self.game_state = ""

                    else:
                        self.window_state = self.board.options_click(pg.mouse.get_pos())
                    
                elif self.window_state == "score":
                    self.window_state = self.scoreboard.click(pg.mouse.get_pos())

            if event.type == pg.QUIT:
                self.quit()
            
    def render(self):
        '''Render window depending on game state'''
        self.window.fill(config.WHITE)

        if self.window_state == "menu":
            self.menu.draw_menu()

        elif self.window_state == "board":
            self.board.draw_board()

            if self.game_state == "win":
                self.board.draw_popup(f"{self.current_player!r} WON")
                self.board.freeze_restart = True
            elif self.game_state == "draw":
                self.board.draw_popup("DRAW!")
                self.board.freeze_restart = True

            else:
                self.board.freeze_restart = False

        elif self.window_state == "score":
            self.scoreboard.draw_scoreboard(self.menu.grid_size)

        pg.display.update()

    def update_game_state(self):
        if self.board.check_win():
            self.pause_grid = True
            self.game_state = "win"
            print(f"Player {self.current_player!r} WON - SCORE: {1 + self.board.open_tile_count}")
        elif self.board.check_draw():
            self.pause_grid = True
            self.game_state = "draw"
            print("DRAW")
        else:
            self.current_player = "O" if self.current_player == "X" else "X"

    def quit(self):
        '''Terminate the program'''
        pg.quit()
        sys.exit()