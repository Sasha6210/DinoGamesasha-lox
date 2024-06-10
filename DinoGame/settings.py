import pygame

class Settings:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.dino_speed = 2
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        