import pygame
from settings import Settings
import random

class Cloud:
    def __init__(self, x, y, width, img, speed):
        self.x = x
        self.y = y
        self.width = width
        self.setting = Settings()
        self.img = img
        self.speed = speed
        self.screen = self.setting.screen

    def cloud_move(self):
        if self.x >= - self.width:
           self.screen.blit(self.img, (self.x, self.y))
           self.x -= self.speed 
        else:
            self.x = self.setting.screen_width

























#        |          -----------------
#        |          |
#        |          |
#        |          |
#        |          |
#        -----------|------------|
#                   |            |
#                   |            |
#                   |            |
#                   |            |
#        ------------