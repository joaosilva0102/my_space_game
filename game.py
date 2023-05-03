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
MENU_FONT = pygame.font.SysFont("comicsans", 40)

pygame.init()

class Ship:
    
    IMG = SHIP
    MAX_BOOST = 100
    
    def __init__(self):
        self.xpos = (SCREEN_WIDTH / 2) - (self.IMG.get_width() / 2)
        self.ypos = SCREEN_HEIGHT - self.IMG.get_height()
        self.health = 30
        self.bullets = []
        self.cooldown = 1
        self.score = 0
        self.boost = 100
        self.can_boost = True
        
        
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
    
    def useBoost(self):
        if self.boost == self.MAX_BOOST or self.can_boost:
            self.boost -= 3
        if self.boost <= 0:
            self.can_boost = False
        
    def restoreBoost(self):
        if self.boost < self.MAX_BOOST:
            self.boost += 1
        if self.boost == 100:
            self.can_boost = True
            
    def canBoost(self):
        return self.can_boost
    
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
        self.ypos = -50
        self.vel = 3
    
    def __del__(self):
        return 0
    
    def move(self):
        self.ypos += self.vel
        
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

class Background:
    IMG = BG
    VEL = 3
    HEIGHT = IMG.get_height()
    
    def __init__(self):
        self.xpos = 0
        self.y1pos = 0
        self.y2pos = -self.HEIGHT
        
    def move(self):
        self.y1pos += self.VEL
        self.y2pos += self.VEL
        
        if self.y1pos > SCREEN_HEIGHT:
            self.y1pos = -self.HEIGHT
        if self.y2pos > SCREEN_HEIGHT:
            self.y2pos = -self.HEIGHT
    
    def draw(self, screen):
        screen.blit(self.IMG, (self.xpos,self.y1pos))
        screen.blit(self.IMG, (self.xpos,self.y2pos))
        
def draw_window(screen, ship, meteors, background):
    
    screen.fill((0,0,0))
    background.draw(screen)
    
    health_gradient = ship.health / 30
    
    pygame.draw.rect(screen, ((1 - health_gradient) * 255, health_gradient * 255, 0), pygame.Rect(10, 10, health_gradient * 150, 30))
    
    score = STAT_FONT.render("Score: " + str(ship.score), 1, (255, 255, 255))
    screen.blit(score, (10, 50))
    
    boost_gradient = ship.boost / 100
    
    pygame.draw.rect(screen, (255,boost_gradient * 255, boost_gradient * 255), pygame.Rect(640, 10, boost_gradient * 150, 30))
    
    ship.draw(screen)
    for proj in ship.bullets:
        proj.draw(screen)
    
    for meteor in meteors:
        meteor.draw(screen)
        
    pygame.display.update()

def start_screen(screen):
    screen.fill((0,0,0))
    text = MENU_FONT.render("Press SPACE to start the game", 1, (255, 255, 255))
    text_rect = text.get_rect(center = (400, 300))
    screen.blit(text, text_rect)                   
    pygame.display.update()  

def game_over_screen(screen, ship):
    screen.fill((0,0,0))
    
    text = MENU_FONT.render("SCORE: " + str(ship.score), 1, (255, 255, 255))
    text_rect = text.get_rect(center = (400, 200))
    screen.blit(text, text_rect)
    
    text = MENU_FONT.render("GAME OVER", 1, (255, 0, 0))
    text_rect = text.get_rect(center = (400, 300))
    screen.blit(text, text_rect)
    
    text = STAT_FONT.render("Press SPACE to play again", 1, (255, 255, 255))
    text_rect = text.get_rect(center = (400, 400))
    screen.blit(text, text_rect)
    pygame.display.update()  
                  
    
def main():
    ship = Ship()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    running = True
    clock = pygame.time.Clock()
    counter = 60
    meteor_timeframe = 80
    next_level = 10
    game_state = "start_menu"
    meteors = []
    
    background = Background()

    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        if game_state == "start_menu":
            start_screen(screen)
            key = pygame.key.get_pressed() 
            if key[pygame.K_SPACE]:
                game_state = "game"
        
        if game_state == "game_over":
            game_over_screen(screen, ship)
            key = pygame.key.get_pressed() 
            if key[pygame.K_SPACE]:
                ship = Ship()
                next_level = 10
                meteors = []
                game_state = "game"   
            
        if game_state == "game":
            background.move()
            key = pygame.key.get_pressed()
            if key[pygame.K_d]:
                if key[pygame.K_LSHIFT] and ship.canBoost():
                    ship.useBoost()
                    ship.moveRight(10)
                else:
                    ship.moveRight(5)               
                    
            if key[pygame.K_a]:
                if key[pygame.K_LSHIFT] and ship.canBoost():
                    ship.useBoost()
                    ship.moveLeft(10)
                else:
                    ship.moveLeft(5)
                    
            ship.restoreBoost()
            
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
            
            for proj in ship.bullets:
                proj.move()    
                
            for meteor in meteors:
                meteor.move()
                
                if meteor.ypos > SCREEN_HEIGHT:
                    ship.hit()
                    meteors.remove(meteor)
                    del meteor
                    
                else:
                    for proj in ship.bullets:
                        if meteor.hit(proj):
                            ship.addScore()
                            ship.bullets.remove(proj)
                            meteors.remove(meteor)
                            del proj
                            del meteor
                            
            if ship.health <= 0:
                game_state = "game_over"
                    
            counter += 1    
            draw_window(screen, ship, meteors, background)  
              
    pygame.quit()
        
main()        