import config
from menu import Menu
from board import Board
import pygame as pg
import sys

class Game:
    def __init__(self):
        pg.init()
        self.window = pg.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        pg.display.set_caption(config.TITLE)
        self.game_state = "menu" # states = [menu, game, scoreboard
        self.menu = Menu(self.window)
        self.board = Board(self.window, self.menu.grid_size)
        self.board.init_tiles()
        self.running = True

    def run(self):
        '''Game runnning loop'''
        while self.running:
            self.events()
            self.render()
        
    def events(self):
        '''Event handler'''
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                pass
            if event.type == pg.QUIT:
                self.quit()
            
    def render(self):
        '''Renter window depending on game state'''
        if self.game_state == "menu":
            self.menu.render_menu()

            if self.menu.start_game:
                self.game_state = "game"

        elif self.game_state == "game":
            self.board.render_board()
        
        elif self.game_state == "scoreboard":
            pass

    def quit(self):
        '''Terminate the program'''
        pg.quit()
        sys.exit()