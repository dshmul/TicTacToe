import config
from menu import Menu
from board import Board
import pygame as pg
import sys
import os

class Game:
    X_IMAGE = pg.image.load(os.path.join('Assets', 'x.png'))
    O_IMAGE = pg.image.load(os.path.join('Assets', 'o.png'))
    PODIUM_IMAGE = pg.image.load(os.path.join('Assets', 'podium.png'))

    # resize images
    X_IMAGE = pg.transform.scale(X_IMAGE, (200,200))
    O_IMAGE = pg.transform.scale(O_IMAGE, (200,200))
    PODIUM_IMAGE = pg.transform.scale(PODIUM_IMAGE, (600 * .80, 600 * .80))


    def __init__(self):
        pg.init()
        self.window = pg.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        pg.display.set_caption(config.TITLE)
        self.game_state = "menu" 
        self.menu = Menu(self.window)
        self.board = Board(self.window, self.menu.grid_size)
        self.board.init_tiles()
        self.running = True

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
                pass
            if event.type == pg.QUIT:
                self.quit()
            
    def render(self):
        '''Render window depending on game state'''
        self.window.fill(config.WHITE)

        if self.game_state == "menu":
            self.menu.draw_menu()
        
            if self.menu.start_game:
                self.game_state = "game"

        elif self.game_state == "game":
            self.board.draw_board()
        
        elif self.game_state == "scoreboard":
            pass

        pg.display.update()

    def quit(self):
        '''Terminate the program'''
        pg.quit()
        sys.exit()