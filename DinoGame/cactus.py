import pygame
import random
from settings import Settings

class Cactus:
    def __init__(self, x, y, width, image, speed):
        self.x = x
        self.y = y
        self.width = width
        self.speed = speed
        self.setting = Settings()
        #self.display_width = self.setting.screen_width
        #self.display_height = self.setting.screen_height
        self.screen = self.setting.screen
        self.image = image
    def move(self):
        if self.x >= self.width:
            self.screen.blit(self.image, (self.x, self.y))
            self.x -= self.speed
            return True
        else:
            return False

    def return_cactus(self, radius, y, width, img):
        self.x = radius
        self.y = y
        self.width = width
        self.image = img
        self.screen.blit(self.image, (self.x, self.y))

    