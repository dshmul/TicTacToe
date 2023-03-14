from src import config
import pygame as pg
import os

class Tile:
    # Class variables
    tile_size = 0

    def __init__(self, row, col):
        self.x = col * Tile.tile_size
        self.y = row * Tile.tile_size
        self.row = row
        self.col = col
        self.marking = None
        self.rect = pg.Rect((self.x, self.y), (Tile.tile_size, Tile.tile_size))

    def draw(self, window):
        pg.draw.rect(window, config.GRAY, self.rect, 4)

        if self.marking == 'X':
            img = pg.image.load(os.path.join('Assets', 'x.png'))
        elif self.marking == 'O':
            img = pg.image.load(os.path.join('Assets', 'o.png'))
        else:
            return
    
        img = pg.transform.scale(img, (Tile.tile_size * config.TILE_SCALE, Tile.tile_size * config.TILE_SCALE))
        img_rect = img.get_rect()
        img_rect.center = self.rect.center
        window.blit(img, img_rect)

    def update_marking(self, marking):
        if not self.marking:
            print(f'Updating tile at (ROW, COL): ({self.row}, {self.col}) to MARKING: {marking!r}')
            self.marking = marking
            return True
        return False

        