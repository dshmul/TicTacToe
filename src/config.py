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
ORANGE = (230, 160, 64)
RED = (255, 0, 0)
DARK_RED = (139, 0, 0)
LIGHT_ORANGE = (255, 213, 128)
LIGHT_GREEN = (132, 247, 82)
YELLOW = (251, 241, 80)

# Presets
EXTRA_BIG_SIZE = 40
TITLE_SIZE = 30
HEADER_SIZE = 20
TEXT_SIZE = 15

EXTRA_BIG_FONT = pg.font.Font(pg.font.get_default_font(), EXTRA_BIG_SIZE)
TITLE_FONT = pg.font.Font(pg.font.get_default_font(), TITLE_SIZE)
HEADER_FONT = pg.font.Font(pg.font.get_default_font(), HEADER_SIZE)
TEXT_FONT = pg.font.Font(pg.font.get_default_font(), TEXT_SIZE)

# API 
API_ADDR = "http://127.0.0.1:5000/"