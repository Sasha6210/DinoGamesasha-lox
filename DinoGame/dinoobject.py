import pygame
from settings import Settings

class DinoObject:
    def __init__(self, ui_game):
        self.setting = Settings()
        self.screen = ui_game.screen
        self.screen_rect = ui_game.screen.get_rect()
        self.image = pygame.image.load('images/Дино 1.png')
        self.images = [pygame.image.load("images/Дино 1.png"), pygame.image.load("images/Дино 2.png")]
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.settings = Settings()
        self.rect.x = 100
        self.rect.y = self.settings.screen_height//2 + 70      
        self.count = 0
        

    def blitme(self):
        if self.count == 12:
            self.count = 0
        self.images[self.count//6] = pygame.transform.scale(self.images[self.count//6], (90, 80))
        self.screen.blit(self.images[self.count//6], self.rect)
        self.count += 1






















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