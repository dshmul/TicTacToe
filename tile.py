import config
import pygame as pg
import os

class Tile:
    # Class variables
    tile_size = 0

    # load images
    X_IMG = pg.image.load(os.path.join('Assets', 'x.png'))
    O_IMG = pg.image.load(os.path.join('Assets', 'o.png'))

    # resize images
    X_IMG = pg.transform.scale(X_IMG, (tile_size, tile_size))
    O_IMG = pg.transform.scale(O_IMG, (tile_size, tile_size))

    def __init__(self, row, col):
        self.x = col * Tile.tile_size
        self.y = row * Tile.tile_size
        self.row = row
        self.col = col
        self.marking = 'X'
        self.rect = pg.Rect((self.x, self.y), (Tile.tile_size, Tile.tile_size))

    def draw(self, window):
        pg.draw.rect(window, config.GRAY, self.rect, 4)
        if self.marking == 'X':
            window.blit(Tile.X_IMG, (self.x, self.y))
        elif self.marking == 'O':
            window.blit(Tile.O_IMG, (self.x, self.y))



        