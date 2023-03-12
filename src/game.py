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
        self.game_state = "menu" 
        self.menu = Menu(self.window)
        self.current_player = self.menu.starting_player
        self.board = Board(self.window, self.menu.grid_size)
        self.board.init_tiles()
        self.running = True
        self.pause_grid = False

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
                if self.game_state == "menu":
                    pass

                if self.game_state == "board":
                    if not self.pause_grid:
                        self.current_player, self.game_state = self.board.click(pg.mouse.get_pos(), self.current_player)
                        
                        if self.board.check_win():
                            self.pause_grid = True
                            print(f"Player {'O' if self.current_player == 'X' else 'X'!r} WON - SCORE: {1 + self.board.open_tile_count}")
                        
                        elif self.board.check_draw():
                            self.pause_grid = True
                            print("DRAW")
                    else:
                        self.board.init_tiles()
                        self.pause_grid = False
                    
                if self.game_state == "score":
                    pass

            if event.type == pg.QUIT:
                self.quit()
            
    def render(self):
        '''Render window depending on game state'''
        self.window.fill(config.WHITE)

        if self.game_state == "menu":
            self.menu.draw_menu()

            if self.menu.start_game:
                self.game_state = "board"

        elif self.game_state == "board":
            self.board.draw_board()

        elif self.game_state == "score":
            pass

        pg.display.update()

    def quit(self):
        '''Terminate the program'''
        pg.quit()
        sys.exit()