import pygame
import os
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 750, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACE INVADER")
RED_SPACE_SHIP = pygame.image.load(os.path.join("space/assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("space/assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("space/assets", "pixel_ship_blue_small.png"))
#Main player
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("space/assets", "pixel_ship_yellow.png"))

RED_LASER =  pygame.image.load(os.path.join("space/assets", "pixel_laser_red.png"))
GREEN_LASER =  pygame.image.load(os.path.join("space/assets", "pixel_laser_green.png"))
BLUE_LASER =  pygame.image.load(os.path.join("space/assets", "pixel_laser_blue.png"))
YELLOW_LASER =  pygame.image.load(os.path.join("space/assets", "pixel_laser_yellow.png"))
NAME =  pygame.image.load(os.path.join("space", "name2.png"))
TITLE =  pygame.image.load(os.path.join("space", "title.png"))


BG = pygame.transform.scale(pygame.image.load(os.path.join("space/assets", "background-black.png")), (WIDTH, HEIGHT))
# transform.scale() helps to enlarge the picture size to fit the screen
LIVE =  pygame.image.load(os.path.join("space", "heart3.png"))
black = (0,0,0)
white = (255,255,255)

red = (200,0,0)
green = (0,200,0)

bright_red = (255,0,0)
bright_green = (0,255,0)

blue = (53,115,255)
pause = False

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
        self.score = 0

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

  

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


class BAR():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def draw(self, window):
        window.blit(LIVE, (self.x , self.y))

class Ship():
    COOLDOWN = 20
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
        
    
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1
            

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
        
    def draw(self, window):
        window.blit(self.ship_img, (self.x,self.y))
        for laser in self.lasers:
            laser.draw(window)

   
    def get_height(self):
        return self.ship_img.get_height()
    
    def get_width(self):
        return self.ship_img.get_width()




class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health) # This allow us to call the attribute form the main class i.e Ship
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img) # Help  to take record of the pixel
        self.max_health = health
        self.score = 0

    def move_laser(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
                        self.score += 1

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)
        
    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (int(self.health)/int(self.max_health)), 10))
       
        
        


class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER) }
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
    def move_laser(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 22, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
        

    def move(self, vel):
        self.y += vel
        
        
# AThis is ued in any collision of object 
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

score = 0



def text_objects(text, font):
    textSurface = font.render(text, True, (255,255,255))
    return textSurface, textSurface.get_rect()


def button(msg,x,y,w,h,ic,ac,action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pygame.draw.rect(WIN, ac, (x,y,w,h))
            if click[0] == 1 and action != None:
                action()
        else:
            pygame.draw.rect(WIN, ic, (x,y,w,h))

        smallText = pygame.font.SysFont("comicsansms",20)
        textSurf, textRect = text_objects(msg, smallText)
        textRect.center = ( (x+(w//2)), (y+(h//2)) )
        WIN.blit(textSurf, textRect)

def quitgame():
    pygame.quit()
    quit()       
clock = pygame.time.Clock()
def unpause():
    global pause
    pause = False

def paused():
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        WIN.blit(BG, (0,0))
        WIN.blit(NAME, (WIDTH/2-100,HEIGHT/2))
        largeText = pygame.font.SysFont("comicsansms",100)
        TextSurf, TextRect = text_objects("Paused", largeText)
        TextRect.center = (int((WIDTH/2)),int((HEIGHT/2) - 100))
        WIN.blit(TextSurf, TextRect)
        # Using the mouse in your program
       
        button("Resume",200,350,150,50,green,bright_green,unpause)
        button("Quit",350,500,150,50,red,bright_red,game_menu())
        


        
        pygame.display.update()
        clock.tick(15)
levels = 0
def main():
    run = True
    FPS = 60
    bar = {0 : True, 1 : True}
    clock = pygame.time.Clock()
    #Lives = 3
    enemies = []
    Level = 0
    wave_length = 5
    enemy_vel = 1
    health_limit = []
    vel = 20
    ranged = [4, 37, 70]
    life_no = 0
    player = Player(300, 550)
    lost = False
    lost_count = 0
    count = 3
    bar_no = 0
    laser_vel = 6
    global pause

    


    
    
    main_font = pygame.font.SysFont("comicsans", 30)
    lost_font = pygame.font.SysFont("comicsans", 70)
    win_font = pygame.font.SysFont("comicsans", 70)
    
    
    
    

    def redraw():
        WIN.blit(BG, (0,0))
        lives_label = main_font.render(f"Score: {player.score} ", 1, (255,255,255))
        level_label = main_font.render(f"level: {Level}", 1, (255,255,255))
        #WIN.blit(LIVE, (5, 5))
        for lifes in health_limit:
            lifes.draw(WIN)
    

        WIN.blit(lives_label, (10, 40))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        for enemy in enemies:
           enemy.draw(WIN)
        
        

        player.draw(WIN)
        if lost:
            lost_label = lost_font.render(f"GAME OVER", 1, (255,255,255))
            WIN.blit(lost_label, (int(WIDTH)//2 - int(lost_label.get_width())//2, 350))
            lives_label = win_font.render(f"Your high Score: {player.score} ", 1, (255,255,255))
            WIN.blit(lives_label, (int(WIDTH)//2 - int(lost_label.get_width())//2 - 20, 450))
            
            

        
        pygame.display.update()


    
    while run:
        clock.tick(FPS)
        redraw()
        if player.health < 0:
            player.health = 100
            health_limit.pop()
            bar_no += 1
        if bar_no == 3:
            player.health = 0
            lost = True
            lost_count += 1
        if lost:
            if lost_count > FPS * 3:
                time.sleep(3)
                game_menu()
            else:
                continue
            
            
                
        if len(health_limit) <= 3 and life_no != 3:
            lifes = BAR(ranged[life_no], 2)
            life_no += 1
            health_limit.append(lifes)
        if len(enemies) == 0:
            Level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if mouse[0] > player.x and player.x < WIDTH - 100:
            player.x += vel
        if mouse[0] < player.x:
            player.x -= vel 
        if click[0] == 1:
             player.shoot()
        if keys[pygame.K_p]:
            pause = True
            paused()
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_laser(laser_vel, player)
            if random.randrange(0, 120) == 1:
                enemy.shoot()
            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT: 
                enemies.remove(enemy)
                player.health -= 10
                
          
        player.move_laser(-laser_vel, enemies)
       
    

def game_menu():

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        WIN.blit(BG, (0,0))
        WIN.blit(TITLE, (-50, 0))
        largeText = pygame.font.SysFont("comicsansms",70)
        TextSurf, TextRect = text_objects("", largeText)
        TextRect.center = (int((WIDTH/2)),int((HEIGHT/2 + 100)))
        WIN.blit(TextSurf, TextRect)
       
        button("Play",200,350,150,50,green,bright_green,main)
        button("Quit",350,500,150,50,red,bright_red,quitgame)
        pygame.display.update()
        clock.tick(15)

game_menu()
#         
    

                


        
            
            
       
        

            
            



main()
