import pygame as pg
import numpy as np
import os

WIDTH, HEIGHT = 600, 700
ROWS = 3
GAP = WIDTH // ROWS
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('TicTacToe')

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

FPS = 60

# load images
X_IMAGE = pg.image.load(os.path.join('Assets', 'x.png'))
O_IMAGE = pg.image.load(os.path.join('Assets', 'o.png'))
PODIUM_IMAGE = pg.image.load(os.path.join('Assets', 'podium.png'))

# resize images
X_IMAGE = pg.transform.scale(X_IMAGE, (GAP * 0.90, GAP * 0.90))
O_IMAGE = pg.transform.scale(O_IMAGE, (GAP * 0.90, GAP * 0.90))
PODIUM_IMAGE = pg.transform.scale(PODIUM_IMAGE, (75, 75))

def draw_window():
    WIN.fill(WHITE)
    draw_grid()
    WIN.blit(X_IMAGE, (GAP * 0, GAP * 0))
    WIN.blit(O_IMAGE, (GAP * 1, GAP * 1))
    WIN.blit(PODIUM_IMAGE, (500, 600))
    pg.display.update()

def init_grid():
    '''Initialize TicTacToe grid
    Returns grid initialized with tile center coordinates (x, y), value (''), and availability (T/F)
    '''
    tile_center = WIDTH // ROWS // 2

    grid = np.zeros(ROWS, ROWS)

    for r in range(len(grid)):
        for c in range(len(grid[0])):
            x = tile_center * (2 * c + 1)
            y = tile_center * (2 * r + 1)
            grid[r][c] = (x, y, '', True)

    return grid

def draw_grid():
    '''Draw grid lines'''
    gap = WIDTH // ROWS

    for i in range(ROWS + 1):
        x = i * gap

        pg.draw.line(WIN, GRAY, (x, 0), (x, WIDTH), 3)
        pg.draw.line(WIN, GRAY, (0, x), (WIDTH, x), 3)

def main():
    clock = pg.time.Clock()
    run = True

    # grid = init_grid()

    while run:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        draw_window()

    pg.quit()

if __name__ == '__main__':
    main()