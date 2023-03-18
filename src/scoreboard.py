from src import config
from src.imageButton import ImageButton
from src.textButton import TextButton
from src.text import Text
import pygame as pg
import requests
from datetime import datetime
from dateutil import tz
import os

pg.init()

class Scoreboard:
    TITLE = "Scoreboard"
    DATE_FORMAT = "%H:%M:%S %d/%m/%y"

    def __init__(self, window, menu):
        self.window = window
        self.menu = menu
        self.scores = []
        self.user = None
        
        # Surfaces
        self.back_img = pg.image.load(os.path.join('assets', 'back.png'))
        self.back_button = ImageButton(self.back_img, 50, 50, 50, 650)

        self.player1_score_button = TextButton("PLACEHOLDER", config.TEXT_FONT, config.BLACK, config.YELLOW_ORANGE, \
                                               175, 50, 200, 650, 25, True)
        self.player2_score_button = TextButton("PLACEHOLDER", config.TEXT_FONT, config.BLACK, config.YELLOW_ORANGE, \
                                               175, 50, 400, 650, 25, True)

        self.podium_img = pg.image.load(os.path.join('assets', 'podium.png'))
        self.podium_button = ImageButton(self.podium_img, 80, 80, 550, 650)

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
        if self.user == None:
            self.draw_text(Scoreboard.TITLE, config.TITLE_FONT, config.BLACK, (config.WINDOW_WIDTH // 2, 75))
            
            pg.draw.line(self.window, config.GRAY, (config.WINDOW_WIDTH // 3, 135), (config.WINDOW_WIDTH // 3, 585), width=4)
            pg.draw.line(self.window, config.GRAY, (config.WINDOW_WIDTH // 3 * 2, 135), (config.WINDOW_WIDTH // 3 * 2, 585), width=4)
            pg.draw.line(self.window, config.GRAY, (config.WINDOW_WIDTH // 21, 185), (config.WINDOW_WIDTH // 21 * 20, 185), width=4)

            Text("Name", config.HEADER_FONT, config.DARK_GRAY, config.WINDOW_WIDTH // 21 * 4, 160).draw(self.window)
            Text("Score", config.HEADER_FONT, config.DARK_GRAY, config.WINDOW_WIDTH // 2, 160).draw(self.window)
            Text("Timestamp", config.HEADER_FONT, config.DARK_GRAY, config.WINDOW_WIDTH // 21 * 17.5, 160).draw(self.window)

            self.draw_text("Name", config.HEADER_FONT, config.DARK_GRAY, (config.WINDOW_WIDTH // 21 * 4, 160))
            self.draw_text("Score", config.HEADER_FONT, config.DARK_GRAY, (config.WINDOW_WIDTH // 2, 160))
            self.draw_text("Timestamp", config.HEADER_FONT, config.DARK_GRAY, (config.WINDOW_WIDTH // 21 * 17.5, 160))

            reply = requests.get(config.API_ADDR + "scoreboard/" + str(grid_size)).json()
            entries = reply["scoreboard"]
            y = 210
            for i, entry in enumerate(entries):
                self.draw_text(i + 1, config.TEXT_FONT, config.BLACK, (15, y))
                self.draw_text(entry["user_name"], config.TEXT_FONT, config.BLACK, (config.WINDOW_WIDTH // 21 * 4, y))
                self.draw_text(entry["score"], config.TEXT_FONT, config.BLACK, (config.WINDOW_WIDTH // 2, y))
                self.draw_text(self.format_dt(entry["date"]), config.TEXT_FONT, config.BLACK, (config.WINDOW_WIDTH // 21 * 17.5, y))
                y += 40
        else:
            self.draw_text(self.user.username, config.TITLE_FONT, config.BLACK, (config.WINDOW_WIDTH // 2, 75))

            pg.draw.line(self.window, config.GRAY, (config.WINDOW_WIDTH // 2, 135), (config.WINDOW_WIDTH // 2, 585), width=4)
            pg.draw.line(self.window, config.GRAY, (115, 185), (450, 185), width=4)

            self.draw_text("Timestamp", config.HEADER_FONT, config.DARK_GRAY, (config.WINDOW_WIDTH // 4 + 50, 160))
            self.draw_text("Score", config.HEADER_FONT, config.DARK_GRAY, (config.WINDOW_WIDTH // 4 * 3 - 75, 160))

            reply = requests.get(config.API_ADDR + "score", headers={"x-access-token": self.user.token}).json()
            entries = reply["scores"]
            y = 210
            for entry in entries:
                self.draw_text(self.format_dt(entry["date"]), config.TEXT_FONT, config.BLACK, (config.WINDOW_WIDTH // 4 + 50, y))
                self.draw_text(entry["score"], config.TEXT_FONT, config.BLACK, (config.WINDOW_WIDTH // 4 * 3 - 75, y))
                y += 40
            
        self.back_button.draw(self.window)

        if self.menu.player1.logged_in:
            self.player1_score_button.update_text(f"{self.menu.player1.username!r} Scores")
            self.player1_score_button.draw(self.window)

        if self.menu.player2.logged_in:
            self.player2_score_button.update_text(f"{self.menu.player2.username!r} Scores")
            self.player2_score_button.draw(self.window)

        self.podium_button.draw(self.window)

    def click(self, mouse_pos):
        x, y = mouse_pos
        if self.back_button.button_rect.collidepoint(x, y):
            self.user = None
            return "board"
        elif self.podium_button.button_rect.collidepoint(x, y):
            self.user = None
        elif self.menu.player1.logged_in and self.player1_score_button.button_rect.collidepoint(x, y):
            self.user = self.menu.player1
        elif self.menu.player2.logged_in and self.player2_score_button.button_rect.collidepoint(x, y):
            self.user = self.menu.player2

        return "score"