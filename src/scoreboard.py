from src import config
from src.menu import Menu
from src.inputBox import InputBox
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
        self.back_img = pg.image.load(os.path.join('Assets', 'back.png'))
        self.back_button = pg.transform.scale(self.back_img, (50, 50))
        self.back_button_rect = self.back_button.get_rect()
        self.back_button_rect.center = (50, 650)

        self.player1_button_rect = pg.Rect((0, 0), (175, 50))
        self.player1_button_border = pg.Rect((0, 0), (175, 50))
        self.player1_button_rect.center = (200, 650)
        self.player1_button_border.center = (200, 650)

        self.player2_button_rect = pg.Rect((0, 0), (175, 50))
        self.player2_button_border = pg.Rect((0, 0), (175, 50))
        self.player2_button_rect.center = (400, 650)
        self.player2_button_border.center = (400, 650)

        self.podium_img = pg.image.load(os.path.join('Assets', 'podium.png'))
        self.podium_button = pg.transform.scale(self.podium_img, (80, 80))
        self.podium_button_rect = self.podium_button.get_rect()
        self.podium_button_rect.center = (550, 650)

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
            
        self.window.blit(self.back_button, self.back_button_rect)

        pg.draw.rect(self.window, config.YELLOW_ORANGE, self.player1_button_rect, 25, 5, 5, 5, 5)
        pg.draw.rect(self.window, config.BLACK, self.player1_button_rect, 1, 5, 5, 5, 5)
        self.draw_text(f"{self.menu.player1.username!r} Scores", config.TEXT_FONT, config.BLACK, self.player1_button_rect.center)

        pg.draw.rect(self.window, config.YELLOW_ORANGE, self.player2_button_rect, 25, 5, 5, 5, 5)
        pg.draw.rect(self.window, config.BLACK, self.player2_button_rect, 1, 5, 5, 5, 5)
        self.draw_text(f"{self.menu.player2.username!r} Scores", config.TEXT_FONT, config.BLACK, self.player2_button_rect.center)

        self.window.blit(self.podium_button, self.podium_button_rect)

    def update_player_names(self):
        self.player1_username_text = config.TEXT_FONT.render(f"{self.menu.player1.username!r} Scores", True, config.BLACK)
        self.player2_username_text = config.TEXT_FONT.render(f"{self.menu.player2.username!r} Scores", True, config.BLACK)

    def click(self, mouse_pos):
        x, y = mouse_pos
        if self.back_button_rect.collidepoint(x, y):
            self.user = None
            return "board"
        elif self.podium_button_rect.collidepoint(x, y):
            self.user = None
        elif self.player1_button_rect.collidepoint(x, y):
            self.user = self.menu.player1
        elif self.player2_button_rect.collidepoint(x, y):
            self.user = self.menu.player2

        return "score"