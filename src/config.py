import pygame as pg
pg.init()

# Display settings
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700
TILE_SCALE = 0.85
TITLE = "Tic Tac Toe"
FPS = 60

# Preset colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (128, 128, 128)
GRAY = (200, 200, 200)
DARK_GRAY = (95, 95, 95)
BLUE = (173, 216, 230)

# Presets
TITLE_SIZE = 30
HEADER_SIZE = 20
TEXT_SIZE = 15

TITLE_FONT = pg.font.Font(pg.font.get_default_font(), TITLE_SIZE)
HEADER_FONT = pg.font.Font(pg.font.get_default_font(), HEADER_SIZE)
TEXT_FONT = pg.font.Font(pg.font.get_default_font(), TEXT_SIZE)

# API 
API_ADDR = "http://127.0.0.1:8000/"