from src import config
from src.inputBox import InputBox
from src.imageButton import ImageButton
from src.textButton import TextButton
from src.text import Text
from src.user import User
import pygame as pg
import requests
import os

class Menu:
    TITLE_SCALE_FACTOR = 0.40
    START_BUTTON_SCALE_FACTOR = 0.125

    def __init__(self, window):
        self.window = window
        self.grid_size = 3
        self.starting_player = 'X'
        self.api_connection = False
        self.start_game = False
        self.active_input = None

        self.player1 = User('X')
        self.player2 = User('O')

        # General Surfaces
        self.title_img = pg.image.load(os.path.join('assets', 'tictactoe.png'))
        self.title = ImageButton(self.title_img, self.title_img.get_width() * Menu.TITLE_SCALE_FACTOR, \
                                 self.title_img.get_height() * Menu.TITLE_SCALE_FACTOR, config.WINDOW_WIDTH // 2, 100)
        self.title_gray_img = pg.image.load(os.path.join('assets', 'tictactoe_gray.png'))
        self.title_gray = ImageButton(self.title_gray_img, self.title_img.get_width() * Menu.TITLE_SCALE_FACTOR, \
                                 self.title_img.get_height() * Menu.TITLE_SCALE_FACTOR, config.WINDOW_WIDTH // 2, 100)

        self.start_img = pg.image.load(os.path.join('assets', 'start.png'))
        self.start_button = ImageButton(self.start_img, self.start_img.get_width() * Menu.START_BUTTON_SCALE_FACTOR,\
                                        self.start_img.get_height() * Menu.START_BUTTON_SCALE_FACTOR, config.WINDOW_WIDTH // 2, 635)        
        self.start_gray_img = pg.image.load(os.path.join('assets', 'start_gray.png'))
        self.start_gray_button = ImageButton(self.start_gray_img, self.start_img.get_width() * Menu.START_BUTTON_SCALE_FACTOR,\
                                        self.start_img.get_height() * Menu.START_BUTTON_SCALE_FACTOR, config.WINDOW_WIDTH // 2, 635)

        # Surfaces before login
        self.username1_input = InputBox(config.WINDOW_WIDTH * 0.25, 250, 200, 50, "username") 
        self.username2_input = InputBox(config.WINDOW_WIDTH * 0.75, 250, 200, 50, "username")
        self.password1_input = InputBox(config.WINDOW_WIDTH * 0.25, 315, 200, 50, "password")
        self.password2_input = InputBox(config.WINDOW_WIDTH * 0.75, 315, 200, 50, "password")

        self.register1_button = TextButton("Register", config.HEADER_FONT, config.BLACK, config.LIGHT_ORANGE, \
                                           200, 50, config.WINDOW_WIDTH * 0.25, 380, 25, True)
        self.register2_button = TextButton("Register", config.HEADER_FONT, config.BLACK, config.LIGHT_ORANGE, \
                                           200, 50, config.WINDOW_WIDTH * 0.75, 380, 25, True)
        
        self.guest1_button = TextButton("Guest", config.HEADER_FONT, config.BLACK, config.LIGHT_ORANGE, \
                                        200, 50, config.WINDOW_WIDTH * 0.25, 445, 25, True)
        self.guest2_button = TextButton("Guest", config.HEADER_FONT, config.BLACK, config.LIGHT_ORANGE, \
                                        200, 50, config.WINDOW_WIDTH * 0.75, 445, 25, True)

        # Surfaces after login
        self.cover1_rect = pg.Rect((0, 0), (275, 275))
        self.cover1_rect.center = (config.WINDOW_WIDTH * 0.25, 345)
        self.cover2_rect = pg.Rect((0, 0), (275, 275))
        self.cover2_rect.center = (config.WINDOW_WIDTH * 0.75, 345)

        self.username1 = Text("PLACEHOLDER", config.HEADER_FONT, config.BLACK, config.WINDOW_WIDTH * 0.25, 315)
        self.username2 = Text("PLACEHOLDER", config.HEADER_FONT, config.BLACK, config.WINDOW_WIDTH * 0.75, 315)

        self.logout1_button = TextButton("Logout", config.HEADER_FONT, config.BLACK, config.LIGHT_ORANGE, \
                                         200, 50, config.WINDOW_WIDTH * 0.25, 380, 25, True)
        self.logout2_button = TextButton("Logout", config.HEADER_FONT, config.BLACK, config.LIGHT_ORANGE, \
                                         200, 50, config.WINDOW_WIDTH * 0.75, 380, 25, True)

        # Surfaces for grid size selection
        self.grid3_button = TextButton("3x3", config.HEADER_FONT, config.BLACK, config.GRAY, \
                                       75, 50, config.WINDOW_WIDTH * 0.4, 540, 25, True)
        self.grid10_button = TextButton("10x10", config.HEADER_FONT, config.BLACK, config.GRAY, \
                                       75, 50, config.WINDOW_WIDTH * 0.6, 540, 25, True)
        
    def draw_menu(self):
        try: 
            reply = requests.get(config.API_ADDR + "/")
            if reply.status_code != 200:
                raise Exception("Unable to access API.")
            
            self.title.draw(self.window)
            self.api_connection = True

            if self.player1.logged_in:
                self.player1.validate_token()
            if self.player2.logged_in:
                self.player2.validate_token()
        except:
            self.title_gray.draw(self.window)
            self.api_connection = False

        if self.start_game and self.api_connection and self.player1.logged_in and self.player2.logged_in:
            self.start_button.draw(self.window)
        else:
            self.start_gray_button.draw(self.window)

        pg.draw.line(self.window, config.GRAY, (config.WINDOW_WIDTH // 2, 210), (config.WINDOW_WIDTH // 2, 485), width=4)

        if not self.player1.logged_in:
            self.username1_input.draw(self.window)
            self.password1_input.draw(self.window)
            self.register1_button.draw(self.window)
            self.guest1_button.draw(self.window)
        else:
            pg.draw.rect(self.window, config.WHITE, self.cover1_rect)
            
            self.username1.draw(self.window)
            self.logout1_button.draw(self.window)

        if not self.player2.logged_in:
            self.username2_input.draw(self.window)
            self.password2_input.draw(self.window)
            self.register2_button.draw(self.window)
            self.guest2_button.draw(self.window)
        else:
            pg.draw.rect(self.window, config.WHITE, self.cover2_rect)

            self.username2.draw(self.window)
            self.logout2_button.draw(self.window)

        if self.grid_size == 3:
            self.grid3_button.draw(self.window, config.BLUE)
            self.grid10_button.draw(self.window, config.GRAY)
        else:
            self.grid3_button.draw(self.window, config.GRAY)
            self.grid10_button.draw(self.window, config.BLUE)
        
    def click(self, mouse_pos): 
        x, y = mouse_pos

        if self.username1_input.entry_rect.collidepoint(x, y):
            self.active_input = self.username1_input
            self.username1_input.active = True
            self.username2_input.active = False
            self.password1_input.active = False
            self.password2_input.active = False
        elif self.username2_input.entry_rect.collidepoint(x, y):
            self.active_input = self.username2_input
            self.username1_input.active = False
            self.username2_input.active = True
            self.password1_input.active = False
            self.password2_input.active = False
        elif self.password1_input.entry_rect.collidepoint(x, y):
            self.active_input = self.password1_input
            self.username1_input.active = False
            self.username2_input.active = False
            self.password1_input.active = True
            self.password2_input.active = False
        elif self.password2_input.entry_rect.collidepoint(x, y):
            self.active_input = self.password2_input
            self.username1_input.active = False
            self.username2_input.active = False
            self.password1_input.active = False
            self.password2_input.active = True
        else:
            self.active_input = None
            self.username1_input.active = False
            self.username2_input.active = False
            self.password1_input.active = False
            self.password2_input.active = False
        
        if not self.player1.logged_in:
            if self.register1_button.button_rect.collidepoint(x, y) and self.username1_input.input and self.password1_input.input:
                self.player1.register(self.username1_input.input, self.password1_input.input)

                if not self.player1.token:
                    self.username1_input.invalid = True
                    self.password1_input.invalid = True
                else:
                    self.username1_input.invalid = False
                    self.password1_input.invalid = False
            elif self.guest1_button.button_rect.collidepoint(x, y):
                self.player1.register("Guest", "guest")
            self.username1.update_text(self.player1.username)
        else:
            if self.logout1_button.button_rect.collidepoint(x, y):
                self.player1.logout()

        if not self.player2.logged_in:
            if self.register2_button.button_rect.collidepoint(x, y) and self.username2_input.input and self.password2_input.input:
                self.player2.register(self.username2_input.input, self.password2_input.input)
                
                if not self.player2.token:
                    self.username2_input.invalid = True
                    self.password2_input.invalid = True
                else:
                    self.username2_input.invalid = False
                    self.password2_input.invalid = False
            elif self.guest2_button.button_rect.collidepoint(x, y):
                self.player2.register("Guest", "guest")
            self.username2.update_text(self.player2.username)
        else:
            if self.logout2_button.button_rect.collidepoint(x, y):
                self.player2.logout()

        if self.player1.logged_in and self.player2.logged_in:
            self.start_game = True
        else:
            self.start_game = False

        if self.grid_size == 10 and self.grid3_button.button_rect.collidepoint(x, y):
            self.grid_size = 3
            return "update_board"
        elif self.grid_size == 3 and self.grid10_button.button_rect.collidepoint(x, y):
            self.grid_size = 10
            return "update_board"
            
        if self.start_button.button_rect.collidepoint(x, y) and self.start_game:
            return "board"
        return "menu"
