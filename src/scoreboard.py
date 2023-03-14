from src import config
from src.menu import Menu
import pygame as pg
import requests
from datetime import datetime
from dateutil import tz
import os

pg.init()

class Scoreboard:
    TITLE = "Scoreboard"
    DATE_FORMAT = "%H:%M:%S %d/%m/%y"

    def __init__(self, window):
        self.window = window
        self.scores = []
        
        self.back_img = pg.image.load(os.path.join('Assets', 'back.png'))
        self.back_button = pg.transform.scale(self.back_img, (50, 50))
        self.back_button_rect = self.back_button.get_rect()
        self.back_button_rect.center = (50, 650)

    def format_dt(self, dt_str):
        dt_utc = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S.%f")
        dt_local = dt_utc.astimezone(tz.tzlocal())
        return dt_local.strftime(Scoreboard.DATE_FORMAT)
    
    def draw_text(self, text, text_font, text_color, center_coordinates):
        text = text_font.render(str(text), True, text_color)
        text_rect = text.get_rect()
        text_rect.center = center_coordinates
        self.window.blit(text, text_rect)

    def draw_scoreboard(self, grid_size):
        self.draw_text(Scoreboard.TITLE, config.TITLE_FONT, config.BLACK, (config.WINDOW_WIDTH // 2, 75))
        
        pg.draw.line(self.window, config.GRAY, (config.WINDOW_WIDTH // 3, 150), (config.WINDOW_WIDTH // 3, 600), width=4)
        pg.draw.line(self.window, config.GRAY, (config.WINDOW_WIDTH // 3 * 2, 150), (config.WINDOW_WIDTH // 3 * 2, 600), width=4)
        pg.draw.line(self.window, config.GRAY, (config.WINDOW_WIDTH // 21, 200), (config.WINDOW_WIDTH // 21 * 20, 200), width=4)

        self.draw_text("Name", config.HEADER_FONT, config.DARK_GRAY, (config.WINDOW_WIDTH // 21 * 4, 175))
        self.draw_text("Score", config.HEADER_FONT, config.DARK_GRAY, (config.WINDOW_WIDTH // 2, 175))
        self.draw_text("Timestamp", config.HEADER_FONT, config.DARK_GRAY, (config.WINDOW_WIDTH // 21 * 17.5, 175))

        request = requests.get(config.API_ADDR + "/scoreboard/" + str(grid_size)).json()
        entries = request["scoreboard"]
        y = 225
        for i, entry in enumerate(entries):
            self.draw_text(i + 1, config.TEXT_FONT, config.BLACK, (15, y))
            self.draw_text(entry["user_name"], config.TEXT_FONT, config.BLACK, (config.WINDOW_WIDTH // 21 * 4, y))
            self.draw_text(entry["score"], config.TEXT_FONT, config.BLACK, (config.WINDOW_WIDTH // 2, y))
            self.draw_text(self.format_dt(entry["date"]), config.TEXT_FONT, config.BLACK, (config.WINDOW_WIDTH // 21 * 17.5, y))
            y += 40
        
        self.window.blit(self.back_button, self.back_button_rect)

    def click(self, mouse_pos):
        x, y = mouse_pos
        if self.back_button_rect.collidepoint(x, y):
            return "board"
        return "score"