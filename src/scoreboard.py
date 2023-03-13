import config
import pygame as pg
import requests
from datetime import datetime
from dateutil import tz

pg.init()

class Scoreboard:
    TITLE = "Scoreboard"
    TITLE_FONT = pg.font.Font(pg.font.get_default_font(), config.TITLE_SIZE)
    HEADER_FONT = pg.font.Font(pg.font.get_default_font(), config.HEADER_SIZE)
    TEXT_FONT = pg.font.Font(pg.font.get_default_font(), config.TEXT_SIZE)
    DATE_FORMAT = "%H:%M:%S %d/%m/%y"

    def __init__(self, window):
        self.window = window
        self.scores = []

    def format_dt(self, dt_str):
        dt_utc = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S.%f")
        dt_local = dt_utc.astimezone(tz.tzlocal())
        return dt_local.strftime(Scoreboard.DATE_FORMAT)
    
    def draw_text(self, text, text_font, text_color, center_coordinates):
        text= text_font.render(str(text), True, text_color)
        text_rect = text.get_rect()
        text_rect.center = center_coordinates
        self.window.blit(text, text_rect)

    def draw_scoreboard(self):
        self.draw_text(Scoreboard.TITLE, Scoreboard.TITLE_FONT, config.BLACK, (config.WINDOW_WIDTH // 2, 75))
        
        pg.draw.line(self.window, config.GRAY, (config.WINDOW_WIDTH // 3, 150), (config.WINDOW_WIDTH // 3, 600), width=4)
        pg.draw.line(self.window, config.GRAY, (config.WINDOW_WIDTH // 3 * 2, 150), (config.WINDOW_WIDTH // 3 * 2, 600), width=4)
        pg.draw.line(self.window, config.GRAY, (config.WINDOW_WIDTH // 21, 200), (config.WINDOW_WIDTH // 21 * 20, 200), width=4)

        self.draw_text("Name", Scoreboard.HEADER_FONT, config.DARK_GRAY, (config.WINDOW_WIDTH // 21 * 4, 175))
        self.draw_text("Score", Scoreboard.HEADER_FONT, config.DARK_GRAY, (config.WINDOW_WIDTH // 2, 175))
        self.draw_text("Timestamp", Scoreboard.HEADER_FONT, config.DARK_GRAY, (config.WINDOW_WIDTH // 21 * 17.5, 175))

        request = requests.get(config.API_ADDR + "/scoreboard/3").json()
        entries = request["scoreboard"]
        y = 225
        for i, entry in enumerate(entries):
            self.draw_text(i + 1, Scoreboard.TEXT_FONT, config.BLACK, (15, y))
            self.draw_text(entry["user_name"], Scoreboard.TEXT_FONT, config.BLACK, (config.WINDOW_WIDTH // 21 * 4, y))
            self.draw_text(entry["score"], Scoreboard.TEXT_FONT, config.BLACK, (config.WINDOW_WIDTH // 2, y))
            self.draw_text(self.format_dt(entry["date"]), Scoreboard.TEXT_FONT, config.BLACK, (config.WINDOW_WIDTH // 21 * 17.5, y))
            y += 40
        