import pygame
import sys
from time import monotonic
from dinoobject import DinoObject
from settings import Settings
import random
from cactus import Cactus
from cloud import Cloud

class Button():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_color = (13, 162, 58)
        self.active_color = (63, 224, 7)
        self.setting = Settings()
        self.screen = self.setting.screen
        self.btn_sound = pygame.mixer.Sound("Accomp_A.ogg")

    def draw(self, x, y, action = None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        pygame.draw.rect(self.screen, self.inactive_color,(x, y, self.width, self.height))
        if x < mouse[0] < x + self.width:
            if y < mouse[1] < y + self.height:
                pygame.draw.rect(self.screen, self.active_color, (x, y, self.width, self.height))
                if click[0] == 1:
                    pygame.mixer.Sound.play(self.btn_sound)
                    pygame.time.delay(300)
                    if action is not None:
                        action()



class DinoGame():
    """rthedfyyz htcehcfvb"""
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = self.settings.screen
        icon = pygame.image.load("images/Дино 1.png")
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Dino Ball Run")
        
        self.dinosaur = DinoObject(self)
        
        self.make_jump = False
        self.counter_jump = 30
        self.usr_width = 80
        self.usr_height = 80
        self.usr_x = self.settings.screen_width//3
        self.usr_y = self.settings.screen_height - self.usr_height - 100
        self.cactus_arr = []
        self.clock = pygame.time.Clock()
        self.cactus_images = [pygame.image.load('images/Кактус 1.png'), pygame.image.load('images/Кактус 2.png'), pygame.image.load('images/Кактус 3.png')]
        self.cactus_size = [80, 391, 80, 380, 80, 380]
        self.cloud_img = [pygame.image.load('images/Хмара 1.png'), pygame.image.load('images/Хмара 2.png')]
        self.back = pygame.image.load('images/лінія.png')
        self.cloud_width = 80
        self.clouds = []
        self.showmenu = True
        self.menu_image = pygame.image.load('images/DESERT.png')

        self.jump_soud = pygame.mixer.Sound('Удар тыщ (для видеомонтажа).mp3')
        pygame.mixer.music.load("Accomp_A.ogg")
        pygame.mixer.music.set_volume(0.3)
        

        self.scores = 0
        self.max_score = 0
        self.above_cactus = False
    def show_menu(self):
        start_btn = Button(200, 50)
        exit_btn = Button(200, 50)
        while self.showmenu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            self.screen.blit(self.menu_image, (0, 0))
            self.print_text("DINO BALL RUN", 450, 100)
            start_btn.draw(470, 300, self.run_game)
            self.print_text("START GAME", 500, 300)
            exit_btn.draw(470, 380, quit)
            self.print_text("QUIT GAME", 500, 380)
            pygame.display.update()
    def run_game(self):
        pygame.mixer.music.play(-1)
        self.array_cactus()  
        for i in range(4):
            y = random.randint(0, 60)
            x = random.randint(self.settings.screen_width//2,self.settings.screen_width)
            choise = random.randint(0, 1) 
            self.clouds.append(Cloud(x, y, self.cloud_width, self.cloud_img[choise], 2))  
            mode_game = True  
        t = monotonic()
        while True:
            if (monotonic() - t) > 1:
                t = monotonic()
                self.scores += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.make_jump = True
            if self.make_jump:
                self.jump()
            if keys[pygame.K_ESCAPE]:
                self.paused()
            self.screen.blit(self.back, (0, 0))

            self.print_text("Scores: " + str(self.scores), 800, 10)
            if monotonic() - t > 1:
                self.scores += 1
                t = monotonic()
            self.print_text("scores: " + str(self.scores), 600, 10)
            self.dinosaur.blitme() 
            self.draw_cactus_arr()
            if self.chek_collision():
                pygame.mixer.music.stop()
                if self.scores > self.max_score:
                    self.max_score = self.scores
                self.print_text('Game over, press Enter to play again Ecs to exit', 125, 300)
                self.print_text('Max scores ' + str(self.max_score), 225, 340)
                pygame.display.update()
                mode_game = self.game_over()
            pygame.display.update()
            #self.clock.tick(65)
            for cl in self.clouds:
                cl.cloud_move()
            pygame.display.flip()
            self.clock.tick(60)
            
    
    def jump(self):
        if self.counter_jump >= -30:
            if self.counter_jump == 30:
                pygame.mixer.Sound.play(self.jump_soud)
            self.dinosaur.rect.y -= self.counter_jump//2.5
            self.counter_jump -= 1
        else:
            self.dinosaur.rect.y = self.settings.screen_height//2 + 70
            self.counter_jump = 30
            self.make_jump = False

    def array_cactus(self):
        for i in range(3):
            choise = random.randrange(0,3)
            img = self.cactus_images[choise]
            width = self.cactus_size[choise*2]
            height = self.cactus_size[choise*2+1]
            self.cactus_arr.append(Cactus(self.settings.screen_width+50, height, width, img, 4))  

    def draw_cactus_arr(self):
        for cactus in self.cactus_arr:
            check = cactus.move()
            print(cactus.x)
            if not check:
                radius = self.find_radius()
                choise = random.randrange(0,3)
                img = self.cactus_images[choise]
                width = self.cactus_size[choise*2]
                height = self.cactus_size[choise*2+1]
                cactus.return_cactus(radius, height, width, img)   
        
    def find_radius(self):
        maximum = max([self.cactus_arr[0].x, self.cactus_arr[1].x, self.cactus_arr[2].x])
        if maximum < self.settings.screen_width:
            radius = self.settings.screen_width
            if radius - maximum < 35:
                radius += 150
        else:
            radius = maximum
        choise = random.randrange(0,5)
        if choise == 0:
            radius = random.randrange(10,15)
        else:
            radius = random.randrange(700,800)
        return radius
    
    def print_text(self, message, x, y, font_color = (0, 0, 0), font_type = "font/bionicle-training.ttf", font_size = 13):
        self.message = message
        self.x = x
        self.y = y
        self.font_color = font_color
        self.font_type = pygame.font.Font(font_type, font_size)
        self.message = self.font_type.render(message, True, self.font_color)
        self.screen.blit(self.message, (self.x, self.y))
        #pygame.display.update()
        #self.clock.tick(15)

    def paused(self):
        paused = True
        while paused:   
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            keys = pygame.key.get_pressed()
            self.print_text("Paused, press enter to continue", 125, 300)
            if keys[pygame.K_RETURN]:
                paused = False

    def game_over(self):
        stopped = True
        while stopped:   
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            keys = pygame.key.get_pressed()
            self.print_text("Paused, press enter to continue", 125, 300)
            if keys[pygame.K_RETURN]:
                stopped = False
                self.make_jump = False
                self.cactus_arr = []
                self.counter_jump = 30
                self.clouds = []
                self.dinosaur.rect.y = self.settings.screen_height//2 + 70      

                self.usr_y = self.settings.screen_height - self.usr_height - 100
                self.run_game()
                return True
            if keys[pygame.K_ESCAPE]:
                return False



    def chek_collision(self):
        
        for barrier in self.cactus_arr:
            if not self.make_jump:
                if barrier.x <= self.dinosaur.rect.x+ 40-5 <= barrier.x+barrier.width:
                    print("1//",self.dinosaur.rect.x)
                    print("1//",barrier.x)
                    return True
            elif self.counter_jump == 10:
                if self.dinosaur.rect.y + self.usr_height-5 >= barrier.y:

                    if barrier.x <= self.usr_x + self.usr_width -5<= barrier.x+barrier.width:
                        print("2//",self.dinosaur.rect.x)
                        print("2//",barrier.x)
                        return True
            elif self.counter_jump == -1:
                if self.dinosaur.rect.y + self.usr_height-5 >= barrier.y:
                    if barrier.x <= self.dinosaur.rect.x + self.usr_width -35<= barrier.x+barrier.width:
                        print("3//",self.dinosaur.rect.x)
                        print("3//",barrier.x)
                        return True
            else:
                if self.dinosaur.rect.y + self.usr_height-10 >= barrier.y:
                    if barrier.x <= self.dinosaur.rect.x+5 <= barrier.x + barrier.width:
                        print("4//",self.dinosaur.rect.x)
                        print("4//",barrier.x)
                        return True
        return False
            
    #def count_scores(self):
        
        
        
  
if __name__ == '__main__':
    din = DinoGame()
    din.show_menu()
    #din.run_game()