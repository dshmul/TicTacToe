from src import config
from src.inputBox import InputBox
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
        self.title = pg.transform.scale(self.title_img, (self.title_img.get_width() * Menu.TITLE_SCALE_FACTOR,\
                                                        self.title_img.get_height() * Menu.TITLE_SCALE_FACTOR))
        self.title_rect = self.title.get_rect()
        self.title_rect.center = (config.WINDOW_WIDTH // 2, 100)

        self.title_gray_img = pg.image.load(os.path.join('assets', 'tictactoe_gray.png'))
        self.title_gray = pg.transform.scale(self.title_gray_img, (self.title_gray_img.get_width() * Menu.TITLE_SCALE_FACTOR,\
                                                                   self.title_gray_img.get_height() * Menu.TITLE_SCALE_FACTOR))
        self.title_gray_rect = self.title.get_rect()
        self.title_gray_rect.center = (config.WINDOW_WIDTH // 2, 100)

        self.start_img = pg.image.load(os.path.join('assets', 'start.png'))
        self.start_button = pg.transform.scale(self.start_img, (self.start_img.get_width() * Menu.START_BUTTON_SCALE_FACTOR,\
                                                                self.start_img.get_height() * Menu.START_BUTTON_SCALE_FACTOR))
        self.start_button_rect = self.start_button.get_rect()
        self.start_button_rect.center = (config.WINDOW_WIDTH // 2, 635)
        
        self.start_gray_img = pg.image.load(os.path.join('assets', 'start_gray.png'))
        self.start_gray_button = pg.transform.scale(self.start_gray_img, (self.start_gray_img.get_width() * Menu.START_BUTTON_SCALE_FACTOR,\
                                                                          self.start_gray_img.get_height() * Menu.START_BUTTON_SCALE_FACTOR))
        self.start_gray_button_rect = self.start_gray_button.get_rect()
        self.start_gray_button_rect.center = (config.WINDOW_WIDTH // 2, 635)

        # Surfaces before login
        self.username1_input = InputBox(config.WINDOW_WIDTH * 0.25, 250, 200, 50, "username") 
        self.username2_input = InputBox(config.WINDOW_WIDTH * 0.75, 250, 200, 50, "username")
        self.password1_input = InputBox(config.WINDOW_WIDTH * 0.25, 315, 200, 50, "password")
        self.password2_input = InputBox(config.WINDOW_WIDTH * 0.75, 315, 200, 50, "password")

        self.register1_button_rect = pg.Rect((0, 0), (200, 50))
        self.register1_button_rect.center = (config.WINDOW_WIDTH * 0.25, 380)
        self.register2_button_rect = pg.Rect((0, 0), (200, 50))
        self.register2_button_rect.center = (config.WINDOW_WIDTH * 0.75, 380)

        self.register1_text = config.HEADER_FONT.render("Register", True, config.BLACK)
        self.register1_text_rect = self.register1_text.get_rect()
        self.register1_text_rect.center = self.register1_button_rect.center
        self.register2_text = config.HEADER_FONT.render("Register", True, config.BLACK)
        self.register2_text_rect = self.register2_text.get_rect()
        self.register2_text_rect.center = self.register2_button_rect.center
                
        self.guest1_button_rect = pg.Rect((0, 0), (200, 50))
        self.guest1_button_rect.center = (config.WINDOW_WIDTH * 0.25, 445)
        self.guest2_button_rect = pg.Rect((0, 0), (200, 50))
        self.guest2_button_rect.center = (config.WINDOW_WIDTH * 0.75, 445)

        self.guest1_text = config.HEADER_FONT.render("Guest", True, config.BLACK)
        self.guest1_text_rect = self.guest1_text.get_rect()
        self.guest1_text_rect.center = self.guest1_button_rect.center
        self.guest2_text = config.HEADER_FONT.render("Guest", True, config.BLACK)
        self.guest2_text_rect = self.guest2_text.get_rect()
        self.guest2_text_rect.center = self.guest2_button_rect.center

        # Surfaces after login
        self.cover1_rect = pg.Rect((0, 0), (275, 275))
        self.cover1_rect.center = (config.WINDOW_WIDTH * 0.25, 345)
        self.cover2_rect = pg.Rect((0, 0), (275, 275))
        self.cover2_rect.center = (config.WINDOW_WIDTH * 0.75, 345)

        self.username1_text = config.HEADER_FONT.render("PLACEHOLDER", True, config.BLACK)
        self.username1_text_rect = self.username1_text.get_rect()
        self.username1_text_rect.center = (config.WINDOW_WIDTH * 0.25, 315)
        self.username2_text = config.HEADER_FONT.render("PLACEHOLDER", True, config.BLACK) 
        self.username2_text_rect = self.username2_text.get_rect()
        self.username2_text_rect.center = (config.WINDOW_WIDTH * 0.75, 315)

        self.logout1_button_rect = pg.Rect((0, 0), (200, 50))
        self.logout1_button_rect.center = (config.WINDOW_WIDTH * 0.25, 380)
        self.logout2_button_rect = pg.Rect((0, 0), (200, 50))
        self.logout2_button_rect.center = (config.WINDOW_WIDTH * 0.75, 380)

        self.logout1_text = config.HEADER_FONT.render("Logout", True, config.BLACK)
        self.logout1_text_rect = self.logout1_text.get_rect()
        self.logout1_text_rect.center = self.logout1_button_rect.center
        self.logout2_text = config.HEADER_FONT.render("Logout", True, config.BLACK)
        self.logout2_text_rect = self.logout2_text.get_rect()
        self.logout2_text_rect.center = self.logout2_button_rect.center

        # Surfaces for grid size selection
        self.grid_3_button_rect = pg.Rect((0, 0), (75, 50))
        self.grid_3_button_rect.center = (config.WINDOW_WIDTH * 0.4, 540)
        self.grid_10_button_rect = pg.Rect((0, 0), (75, 50))
        self.grid_10_button_rect.center = (config.WINDOW_WIDTH * 0.6, 540)

        self.grid_3_text = config.HEADER_FONT.render("3x3", True, config.BLACK)
        self.grid_3_text_rect = self.grid_3_text.get_rect()
        self.grid_3_text_rect.center = self.grid_3_button_rect.center
        self.grid_10_text = config.HEADER_FONT.render("10x10", True, config.BLACK)
        self.grid_10_text_rect = self.grid_10_text.get_rect()
        self.grid_10_text_rect.center = self.grid_10_button_rect.center

    def draw_menu(self):
        try: 
            requests.get(config.API_ADDR + "/")
            self.window.blit(self.title, self.title_rect)
            self.api_connection = True

            if self.player1.logged_in:
                self.player1.validate_token()
            if self.player2.logged_in:
                self.player2.validate_token()
        except:
            self.window.blit(self.title_gray, self.title_gray_rect)
            self.api_connection = False

        if self.start_game and self.api_connection and self.player1.logged_in and self.player2.logged_in:
            self.window.blit(self.start_button, self.start_button_rect)
        else:
            self.window.blit(self.start_gray_button, self.start_gray_button_rect)

        pg.draw.line(self.window, config.GRAY, (config.WINDOW_WIDTH // 2, 210), (config.WINDOW_WIDTH // 2, 485), width=4)

        if not self.player1.logged_in:
            self.username1_input.draw(self.window)
            self.password1_input.draw(self.window)
            pg.draw.rect(self.window, config.LIGHT_ORANGE, self.register1_button_rect, 25, 5, 5, 5, 5)
            self.window.blit(self.register1_text, self.register1_text_rect)
            pg.draw.rect(self.window, config.LIGHT_ORANGE, self.guest1_button_rect, 25, 5, 5, 5, 5)
            self.window.blit(self.guest1_text, self.guest1_text_rect)
        else:
            pg.draw.rect(self.window, config.WHITE, self.cover1_rect)

            self.window.blit(self.username1_text, self.username1_text_rect)
            pg.draw.rect(self.window, config.LIGHT_ORANGE, self.logout1_button_rect, 25, 5, 5, 5, 5)
            self.window.blit(self.logout1_text, self.logout1_text_rect)

        if not self.player2.logged_in:
            self.username2_input.draw(self.window)
            self.password2_input.draw(self.window)
            pg.draw.rect(self.window, config.LIGHT_ORANGE, self.register2_button_rect, 25, 5, 5, 5, 5)
            self.window.blit(self.register2_text, self.register2_text_rect)
            pg.draw.rect(self.window, config.LIGHT_ORANGE, self.guest2_button_rect, 25, 5, 5, 5, 5)
            self.window.blit(self.guest2_text, self.guest2_text_rect)
        else:
            pg.draw.rect(self.window, config.WHITE, self.cover2_rect)

            self.window.blit(self.username2_text, self.username2_text_rect)
            pg.draw.rect(self.window, config.LIGHT_ORANGE, self.logout2_button_rect, 25, 5, 5, 5, 5)
            self.window.blit(self.logout2_text, self.logout2_text_rect)

        if self.grid_size == 3:
            pg.draw.rect(self.window, config.BLUE, self.grid_3_button_rect, 25, 5, 5, 5, 5)
            pg.draw.rect(self.window, config.GRAY, self.grid_10_button_rect, 25, 5, 5, 5, 5)
        else:
            pg.draw.rect(self.window, config.GRAY, self.grid_3_button_rect, 25, 5, 5, 5, 5)
            pg.draw.rect(self.window, config.BLUE, self.grid_10_button_rect, 25, 5, 5, 5, 5)

        self.window.blit(self.grid_3_text, self.grid_3_text_rect)
        self.window.blit(self.grid_10_text, self.grid_10_text_rect)
        
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
            if self.register1_button_rect.collidepoint(x, y) and self.username1_input.input and self.password1_input.input:
                self.player1.register(self.username1_input.input, self.password1_input.input)

                if not self.player1.token:
                    self.username1_input.invalid = True
                    self.password1_input.invalid = True
                else:
                    self.username1_input.invalid = False
                    self.password1_input.invalid = False
            elif self.guest1_button_rect.collidepoint(x, y):
                self.player1.register("Guest", "guest")
            self.username1_text = config.HEADER_FONT.render(self.player1.username, True, config.BLACK)    
        else:
            if self.logout1_button_rect.collidepoint(x, y):
                self.player1.logout()

        if not self.player2.logged_in:
            if self.register2_button_rect.collidepoint(x, y) and self.username2_input.input and self.password2_input.input:
                self.player2.register(self.username2_input.input, self.password2_input.input)
                
                if not self.player2.token:
                    self.username2_input.invalid = True
                    self.password2_input.invalid = True
                else:
                    self.username2_input.invalid = False
                    self.password2_input.invalid = False
            elif self.guest2_button_rect.collidepoint(x, y):
                self.player2.register("Guest", "guest")
            self.username2_text = config.HEADER_FONT.render(self.player2.username, True, config.BLACK)  
        else:
            if self.logout2_button_rect.collidepoint(x, y):
                self.player2.logout()

        if self.player1.logged_in and self.player2.logged_in:
            self.start_game = True
        else:
            self.start_game = False

        if self.grid_size == 10 and self.grid_3_button_rect.collidepoint(x, y):
            self.grid_size = 3
            return "update_board"
        elif self.grid_size == 3 and self.grid_10_button_rect.collidepoint(x, y):
            self.grid_size = 10
            return "update_board"
            
        if self.start_button_rect.collidepoint(x, y) and self.start_game:
            return "board"
        return "menu"
