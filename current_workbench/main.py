import pygame
import random 
from modules.Spaceship import *

SHIP_SIZE = 32
TORPEDO_SIZE = 16
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 800
GAME_WIDTH = 600
GAME_HEIGHT = 800
BLACK = (0,0,0)
WHITE = (255,255,255)

"""
set_mode :
pygame.FULLSCREEN | DOUBLEBUF | OPENGL | HWSURFACE | RESIZABLE | NOFRAME
"""
# pygame.display.Info()
 

"""
 to do list :
 + enlever background images

 """

class Spacebattle:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Spacebattle")
        
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # surface for the game
        self.game_surface = screen.subsurface(pygame.Rect(0,0,GAME_WIDTH,GAME_HEIGHT))
        # surface for score, menu, and other
        self.menu_surface = screen.subsurface(pygame.Rect(GAME_WIDTH,0,SCREEN_WIDTH-GAME_WIDTH,SCREEN_HEIGHT))
        self.menu_surface.fill(WHITE)
        # Player object
        self.player = Spaceship("img/spaceship.png", 4, 100, SCREEN_WIDTH/2,700)
        # list of ennemy objects
        self.ennemys:List[Spaceship] = []

        # Var declaration
        self.running = True
        self.score = 0
        self.last_spawn_ennemy = 0
        self.fps = pygame.time.Clock()
        self.font = pygame.font.Font(None,20)

    def handle_event(self) -> None:
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                self.running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            if self.player.rect.x >= self.player.velocity:
                self.player.move_left()
        if keys[pygame.K_d]:
            if self.player.rect.x < SCREEN_WIDTH-self.player.rect.w:
                self.player.move_right()
        if keys[pygame.K_s]:
            if self.player.rect.y < SCREEN_HEIGHT-self.player.rect.h:
                self.player.move_down()
        if keys[pygame.K_z]:
            if self.player.rect.y >= self.player.velocity:
                self.player.move_up()
        if keys[pygame.K_SPACE]:
            self.player.fire()

    def update(self) -> None:
        if self.last_spawn_ennemy == 0 or pygame.time.get_ticks() - self.last_spawn_ennemy >= 1000:
            for i in range(random.randrange(4,8)):
                self.ennemy_add()
            self.last_spawn_ennemy = pygame.time.get_ticks()

        # ennemy move management
        for elt in self.ennemys:
            elt.move_down()
            if elt.rect.y >= GAME_HEIGHT+SHIP_SIZE:
                self.ennemys.remove(elt)
            if self.player.rect.colliderect(elt.rect):
                self.running = False

        # torpedo move managements
        for elt in self.player.torpedo:
            elt.move()
            if elt.rect.y <= -TORPEDO_SIZE:
                self.player.torpedo.remove(elt)
            for ennemy in self.ennemys:
                if ennemy.rect.colliderect(elt.rect):
                    self.ennemys.remove(ennemy)
                    if self.player.torpedo.index(elt):
                        self.player.torpedo.remove(elt)
                    self.score += 100

    def display(self) -> None:
        
        # game surface update
        self.game_surface.fill(BLACK)
        
        for elt in self.player.torpedo:
            self.game_surface.blit(elt.img, elt.rect)
        
        for elt in self.ennemys:
            self.game_surface.blit(elt.img, elt.rect)
        
        self.game_surface.blit(self.player.img, self.player.rect)

        # menu surface update
        self.menu_surface.fill(WHITE)
        
        score_text = self.font.render(f"Score : {self.score}",True, BLACK)
        self.menu_surface.blit(score_text,(10,10))

        pygame.display.flip()

    def run(self):

        while self.running:
            print(self.player.torpedo)
            self.handle_event()

            self.update()

            self.display()

            self.fps.tick(60)        
    
    def ennemy_add(self):
        buffer_ennemy = Spaceship("img/ennemy.png",4,100,random.randrange(0,GAME_WIDTH-SHIP_SIZE),-SHIP_SIZE)
        index = 0
        while index < len(self.ennemys):
            while buffer_ennemy.rect.colliderect(self.ennemys[index].rect):
                buffer_ennemy = Spaceship("img/ennemy.png",4,100,random.randrange(0,GAME_WIDTH-SHIP_SIZE),-SHIP_SIZE)
                index = 0
            index += 1
        self.ennemys.append(buffer_ennemy)


if __name__ == "__main__":
    game = Spacebattle()
    game.run()
