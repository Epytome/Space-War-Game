# Imports
import pygame
import random

# Initialize game engine
pygame.init()


# Window
WIDTH = 1000
HEIGHT = 800
SIZE = (WIDTH, HEIGHT)
TITLE = "Space War"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)


# Timer
clock = pygame.time.Clock()
refresh_rate = 60

#sounds
pygame.mixer.music.load("assets/sounds/oddity.ogg")

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)           
GREEN = (0, 255, 0)

#Fonts
FONT_SM = pygame.font.Font(None, 24)
FONT_MD = pygame.font.Font(None, 32)
FONT_LG = pygame.font.Font(None, 64)
FONT_XL = pygame.font.Font(None, 128)
FONT_Good = pygame.font.Font("assets/fonts/mine.otf", 32)
FONT_God = pygame.font.Font("assets/fonts/mine.otf", 50)
# Images
steve_img = pygame.image.load("assets/steve.PNG")
steve_img = pygame.transform.scale(steve_img, (32, 50))
diamond_img = pygame.image.load("assets/diamond.PNG")
diamond_img = pygame.transform.scale(diamond_img, (20, 20))
ghast_img = pygame.image.load("assets/ghast.PNG")
ghast_img = pygame.transform.scale(ghast_img, (80, 80))
blaze_img = pygame.image.load("assets/blaze.PNG")
blaze_img = pygame.transform.scale(blaze_img, (50, 80))
fire_img = pygame.image.load("assets/fireball.PNG")
fire_img = pygame.transform.scale(fire_img, (30, 30))
nether = pygame.image.load("assets/nether.PNG")
nether = pygame.transform.scale(nether, (1000, 800))
castle = pygame.image.load("assets/castle.PNG")
castle = pygame.transform.scale(castle, (1000, 800))
nethfin = pygame.image.load("assets/nether-fin.PNG")
nethfin = pygame.transform.scale(nethfin, (1000, 800))



#Sounds
ghastnoise = pygame.mixer.Sound("assets/ghastnoise.ogg")
ouchie = pygame.mixer.Sound("assets/Oofy.ogg")
bam = pygame.mixer.Sound("assets/bam.ogg")

#Stages
START = 0
PLAYING = 1
END = 2

# Game classes

def splash():
    screen.blit(castle, [0,0])


class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.speed = 3
        self.shield = 10
        health = self.shield
                      
    def move_left(self):
        self.rect.x -= self.speed
        
    def move_right(self):
        self.rect.x += self.speed

    def shoot(self):
        laser = Laser(diamond_img)
        laser.rect.centerx = self.rect.centerx
        laser.rect.centery = self.rect.top
        lasers.add(laser)
                   
    def update(self, bombs):
        hit_list = pygame.sprite.spritecollide(self, bombs, True, pygame.sprite.collide_mask) 
        mobhit_list = pygame.sprite.spritecollide(self, mobs, True, pygame.sprite.collide_mask)
        
        for hit in hit_list:
            ouchie.play()
            self.shield -= 1

        for mob in mobhit_list:
            self.shield = 0

        if self.shield == 0:
            bam.play()
            self.kill()
            stage = END




        if self.rect.x >= WIDTH - 32:
            self.rect.x = WIDTH - 32
        elif self.rect.x <= 0:
            self.rect.x = 0

class Laser(pygame.sprite.Sprite):
    
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        
        self.speed = 5

    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.kill()
    
class Mob(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.shield = 10

    def drop_bomb(self):
        bomb = Bomb(fire_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)

    
    def update(self,lasers,player):
        hit_list = pygame.sprite.spritecollide(self, lasers, True, pygame.sprite.collide_mask)


        for hit in hit_list:
            ghastnoise.play()
            player.score += 1
            self.shield -= 1

        if self.shield == 0:
            ouchie.play()
            self.kill()
            



            

class Bomb(pygame.sprite.Sprite):
    
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
    
    
class Fleet:

    def __init__(self, mobs):
        self.mobs = mobs
        self.moving_right = True
        self.speed = 5
        self.bomb_rate = 60

    def move(self):
        reverse = False
        
        for m in mobs:
            if self.moving_right:
                m.rect.x += self.speed
                if m.rect.right >= WIDTH:
                    reverse = True
            else:
                m.rect.x -= self.speed
                if m.rect.left <=0:
                    reverse = True

        if reverse == True:
            self.moving_right = not self.moving_right
            for m in mobs:
                m.rect.y += 32
            

    def choose_bomber(self):
        rand = random.randrange(0, self.bomb_rate)
        all_mobs = mobs.sprites()
        
        if len(all_mobs) > 0 and rand == 0:
            return random.choice(all_mobs)
        else:
            return None
    
    def update(self):
        self.move()

        bomber = self.choose_bomber()
        if bomber != None:
            bomber.drop_bomb()

def setup():
    global ship, mobs, stage, player, bombs, lasers, fleet

    ship = Ship(500, 650, steve_img)

    mob2 = Mob(256, 64, ghast_img)
    mob3 = Mob(384, 64, ghast_img)
    mob4 = Mob(512, 64, ghast_img)
    mob5 = Mob(640, 64, ghast_img)
    mob8 = Mob(268, 140, blaze_img)
    mob9 = Mob(396, 140, blaze_img)
    mob10 = Mob(524, 140, blaze_img)
    mob11 = Mob(652, 140, blaze_img)


    player = pygame.sprite.GroupSingle()
    player.add(ship)
    player.score = 0

    lasers = pygame.sprite.Group()

    mobs = pygame.sprite.Group()
    mobs.add( mob2, mob3, mob4, mob5,  mob8, mob9, mob10, mob11, )

    bombs = pygame.sprite.Group()


    fleet = Fleet(mobs)


    stage = START




            



#Game Help
def show_title_screen():
    title_text = FONT_XL.render("Space War!", 1, WHITE)
    screen.blit(title_text, [280, 204])

def show_stats(player):
    score_text = FONT_Good.render("Score: " + str(player.score), 1, WHITE)
    screen.blit(score_text, [32, 32])



def soundef():
    if stage == START:
        return pygame.mixer.music.load("assets/sounds/menu.ogg")
    elif stage == PLAYING:
        return pygame.mixer.music.load("assets/sounds/oddity.ogg")
    elif stage == END:
        return pygame.mixer.music.load("assets/sounds/nether.ogg")




# Game loop
setup()
done = False


        
while not done:
    if len(mobs) == 0:
        stage = END
        
    # Event processing (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if stage == START:
                if event.key == pygame.K_SPACE:
                    stage = PLAYING
                    soundef()
                    pygame.mixer.music.play(-1)
            elif stage == PLAYING:
                if event.key == pygame.K_SPACE:
                    ship.shoot()
            elif stage == END:
                if event.key == pygame.K_r:
                    setup()

    if stage == PLAYING:

        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_LEFT]:
            ship.move_left()
        elif pressed[pygame.K_RIGHT]:
            ship.move_right()



        
        







    
    # Game logic (Check for collisions, update points, etc.)
    if stage == PLAYING:
        player.update(bombs)
        lasers.update()
        mobs.update(lasers, player)
        bombs.update()
        fleet.update()
        if len(player) == 0:
            stage = END
            soundef()
            pygame.mixer.music.play(-1)
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    if stage == START:
        splash()
        soundef()
        pygame.mixer.music.play(-1)


    if stage == PLAYING:    
        screen.blit(nether, [0,0]) 
        lasers.draw(screen)
        player.draw(screen)
        mobs.draw(screen)
        bombs.draw(screen)
        show_stats(player)

    if stage == END:
        screen.blit(nethfin, [0,0])
        score_txt = FONT_God.render("Congrats you scored: " + str(player.score), 1, WHITE)
        screen.blit(score_txt, [200, HEIGHT/2])

        score_txt = FONT_God.render("Press 'r' to return to title screen!", 1, WHITE)
        screen.blit(score_txt, [40, HEIGHT/2 + 40])


    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
