import pygame as pg

class ImageButton:
    def __init__(self, image, width, height, center_x, center_y):
        self.image_scaled = pg.transform.scale(image, (width, height))
        self.button_rect = self.image_scaled.get_rect()
        self.button_rect.center = (center_x, center_y)

    def draw(self, window):
        window.blit(self.image_scaled, self.button_rect)

    def update_center(self, center_x, center_y):
        self.button_rect.center = (center_x, center_y)