import pygame
import random

pygame.font.init()

SHIP_WIDTH = 70
SHIP_HEIGHT = 70

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

SHIP = pygame.transform.scale(pygame.image.load("ship.png"), (SHIP_WIDTH, SHIP_HEIGHT))
PROJECTILE = pygame.transform.scale(pygame.image.load("projectile.png"), (20, 20))
METEOR = pygame.transform.scale(pygame.image.load("meteorite.png"), (35, 35))
BG = pygame.transform.scale(pygame.image.load("bg.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))

STAT_FONT = pygame.font.SysFont("comicsans", 20)

pygame.init()

class Ship:
    
    IMG = SHIP
    
    def __init__(self):
        self.xpos = (SCREEN_WIDTH / 2) - (self.IMG.get_width() / 2)
        self.ypos = SCREEN_HEIGHT - self.IMG.get_height()
        self.health = 30
        self.bullets = []
        self.cooldown = 0
        self.score = 0
        
        
    def moveLeft(self, moveRate):
        self.xpos -= moveRate
        if self.xpos < -15:
            self.xpos = -15
        
    def moveRight(self, moveRate):
        self.xpos += moveRate
        if self.xpos > SCREEN_WIDTH - self.IMG.get_width() + 15:
            self.xpos = 745
            
    def shootCooldown(self):
        if self.cooldown >= 10:
            self.cooldown = 0
        elif self.cooldown > 0:
            self.cooldown += 1        
            
    def shoot(self):
        if self.cooldown == 0:
            proj = Projectile(self.xpos, self.ypos)
            self.bullets.append(proj)
            self.cooldown = 1          

    def hit(self):
        self.health -= 10
    
    def addScore(self):
        self.score += 1
        
    def draw(self, screen):
        screen.blit(self.IMG, (self.xpos, self.ypos))


class Projectile:
    
    IMG = PROJECTILE
    
    def __init__(self, xpos, ypos):
        self.xpos = xpos + 25
        self.ypos = ypos
    
    def __del__(self):
        return 0
        
    def move(self):
        self.ypos -= 10
    
    def draw(self, screen):
        screen.blit(self.IMG, (self.xpos, self.ypos))
        
    def get_mask(self):
        return pygame.mask.from_surface(self.IMG)

class Meteor:
    
    IMG = METEOR
    
    def __init__(self):
        self.xpos = random.randint(25, SCREEN_WIDTH - 25)
        self.ypos = 0
    
    def __del__(self):
        return 0
    
    def move(self):
        self.ypos += 3
        
    def draw(self, screen):
        screen.blit(self.IMG, (self.xpos, self.ypos))
        
    def hit(self, projectile):
        proj_mask = projectile.get_mask()
        meteor_mask = pygame.mask.from_surface(self.IMG)
        
        offset = (self.xpos - projectile.xpos, self.ypos - projectile.ypos)
        
        overlap = proj_mask.overlap(meteor_mask, offset)
        
        if overlap:
            return True
        
        return False
        
def draw_window(screen, ship, meteors):
    
    screen.fill((0,0,0))
    screen.blit(BG, (0,0))
    
    score = STAT_FONT.render("Score: " + str(ship.score), 1, (255, 255, 255))
    screen.blit(score, (10, 10))
    score = STAT_FONT.render("Health: " + str(ship.health), 1, (255, 255, 255))
    screen.blit(score, (10, 50))
    
    ship.draw(screen)
    for proj in ship.bullets:
        proj.move()
        proj.draw(screen)
    
    for meteor in meteors:
        meteor.move()
        meteor.draw(screen)
        
    pygame.display.update()
    

def main():
    ship = Ship()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    running = True
    clock = pygame.time.Clock()
    counter = 60
    meteor_timeframe = 80
    next_level = 10
            
    meteors = []

    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        key = pygame.key.get_pressed()
        if key[pygame.K_d]:
            if key[pygame.K_LSHIFT]:
                ship.moveRight(10)
            else:
                ship.moveRight(5)
                
        if key[pygame.K_a]:
            if key[pygame.K_LSHIFT]:
                ship.moveLeft(10)
            else:
                ship.moveLeft(5)
                
        if key[pygame.K_SPACE]:
            ship.shoot()
        
        ship.shootCooldown()
        for proj in ship.bullets:
            if proj.ypos < 0:
                ship.bullets.remove(proj)
                del proj
        
        if ship.score == next_level and ship.score <= 50:
            meteor_timeframe -= 10
            next_level += 10
            
        if counter > meteor_timeframe:
            meteor = Meteor()
            meteors.append(meteor)
            counter = 0
            
        for meteor in meteors:
            if meteor.ypos > SCREEN_HEIGHT:
                ship.hit()
                meteors.remove(meteor)
                del meteor
        
            elif ship.health <= 0:
                running = False
                
            else:
                for proj in ship.bullets:
                    if meteor.hit(proj):
                        ship.addScore()
                        ship.bullets.remove(proj)
                        meteors.remove(meteor)
                        del proj
                        del meteor

        counter += 1    
        draw_window(screen, ship, meteors)        
    pygame.quit()
        
main()        