import pygame
import random 
from modules.Spaceship import *
from modules.Button import Button

SHIP_SIZE = 32
TORPEDO_SIZE = 16
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
GAME_WIDTH = SCREEN_WIDTH-100
GAME_HEIGHT = 800
BLACK = (0,0,0)
WHITE = (255,255,255)

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
        
        # button "start"
        self.start_button = Button(50, 30, 20, 20, "Start")
        self.exit_button = Button(50, 30, 20, SCREEN_HEIGHT-50, "Exit")
        
        self.run_menu()
    
    def init_game(self):
        # Player object
        self.player = Spaceship("assets/spaceship.png", 4, 100, SCREEN_WIDTH/2,700)
        # list of ennemy objects
        self.ennemys:List[Spaceship] = []
        
        # Var declaration
        self.running = True
        self.score = 0
        self.last_spawn_ennemy = 0
        self.fps = pygame.time.Clock()
        self.font = pygame.font.Font(None,20)
        self.pause = False

    def run_menu(self):
        run_menu = True
        while run_menu:
            for evt in pygame.event.get():
                if evt.type == pygame.QUIT:
                    run_menu = False
                if evt.type == pygame.MOUSEBUTTONDOWN:
                    abs_offset = self.menu_surface.get_abs_offset()
                    relative_x = evt.pos[0] - abs_offset[0]
                    relative_y = evt.pos[1] - abs_offset[1]
                    if self.start_button.rect.collidepoint(relative_x, relative_y):
                        self.run()
                    if self.exit_button.rect.collidepoint(relative_x, relative_y):
                        run_menu = False                    
            
            self.menu_surface.fill(WHITE)
        
            self.menu_surface.blit(self.start_button.surface, self.start_button.rect)
            self.menu_surface.blit(self.exit_button.surface, self.exit_button.rect)

            pygame.display.flip()
            

    def handle_event(self) -> None:
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                self.running = False
            
            if evt.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.rect.collidepoint(evt.pos):
                    self.start_button.status = not self.start_button.status

            if evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_ESCAPE:
                    self.pause = not self.pause

        if not self.pause:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                if self.player.rect.x >= self.player.velocity:
                    self.player.move_left()
            if keys[pygame.K_d]:
                if self.player.rect.x < GAME_WIDTH-self.player.rect.w:
                    self.player.move_right()
            if keys[pygame.K_s]:
                if self.player.rect.y < GAME_HEIGHT-self.player.rect.h:
                    self.player.move_down()
            if keys[pygame.K_z]:
                if self.player.rect.y >= self.player.velocity:
                    self.player.move_up()
            if keys[pygame.K_SPACE]:
                self.player.fire()

    def update(self) -> None:
        if self.last_spawn_ennemy == 0 or pygame.time.get_ticks() - self.last_spawn_ennemy >= 500:
            self.ennemy_spawn()
            self.last_spawn_ennemy = pygame.time.get_ticks()

        # ennemy move management
        for elt in self.ennemys:
            elt.move_down()
            if elt.rect.y >= GAME_HEIGHT+SHIP_SIZE:
                self.ennemys.remove(elt)
                self.score += 1
            
            # manage collision player and ennemys
            if self.player.rect.colliderect(elt.rect):
                self.player.HP -= 200 

        # torpedo move managements
        for elt in self.player.torpedo:
            elt.move()
            if elt.rect.y <= -TORPEDO_SIZE:
                self.player.torpedo.remove(elt)
            
            # manage collision torpedo and ennemys
            for ennemy in self.ennemys:
                if ennemy.rect.colliderect(elt.rect):
                    ennemy.HP -= elt.damage
                    try:
                        self.player.torpedo.remove(elt) # il y a un probleme ici mais ne sait pas lequel
                    except:
                        pass

                    if ennemy.HP <= 0:
                        self.ennemys.remove(ennemy)
                        self.score += 100
        
        # verify player life
        if self.player.HP <= 0:
            self.running = False
            print(self.score)
            print("End")

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

        self.menu_surface.blit(self.exit_button.surface, self.exit_button.rect)

        pygame.display.flip()

    def run(self):
        self.init_game()
        
        while self.running:
            
            self.handle_event()
            
            if not self.pause:    
                self.update()

                self.display()

                self.fps.tick(60)
            
            if self.pause:
                pygame.time.wait(200)
    
    def ennemy_spawn(self):
        for i in range(random.randrange(4,8)):
            buffer_ennemy = Spaceship("assets/ennemy.png",4,100,random.randrange(0,GAME_WIDTH-SHIP_SIZE),-SHIP_SIZE)
            index = 0
            while index < len(self.ennemys):
                while buffer_ennemy.rect.colliderect(self.ennemys[index].rect):
                    buffer_ennemy = Spaceship("assets/ennemy.png",4,100,random.randrange(0,GAME_WIDTH-SHIP_SIZE),-SHIP_SIZE)
                    index = 0
                index += 1
            self.ennemys.append(buffer_ennemy)
