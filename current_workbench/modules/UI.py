import pygame
import random 
from modules.Spaceship import *
from modules.Button import Button

SHIP_SIZE = 32
TORPEDO_SIZE = 16
BOSS_SIZE = 480
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
GAME_WIDTH = SCREEN_WIDTH-100
GAME_HEIGHT = 800
BG_GAME = (0,0,50)
BG_MENU = (255,255,255)

class Spacebattle:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Spacebattle")
        
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # surface for the game
        self.game_surface = screen.subsurface(pygame.Rect(0,0,GAME_WIDTH,GAME_HEIGHT))
        # surface for score, menu, and other
        self.menu_surface = screen.subsurface(pygame.Rect(GAME_WIDTH,
                                                          0,
                                                          SCREEN_WIDTH-GAME_WIDTH,
                                                          SCREEN_HEIGHT
                                                          )
                                              )
        self.menu_surface.fill(BG_MENU)

        # Player object
        self.player = Spaceship("assets/spaceship.png", GAME_WIDTH/2,GAME_HEIGHT-100)
        
        # button "start"
        self.start_button = Button(50, 30, 20, 20, "Start")
        self.exit_button = Button(50, 30, 20, SCREEN_HEIGHT-50, "Exit")
        
        self.run_menu()
    
    def init_game(self):
        # list of ennemy objects
        self.ennemys:List[Spaceship] = []
        
        # Player object
        self.player = Spaceship("assets/spaceship.png",
                                GAME_WIDTH/2,
                                GAME_HEIGHT-100
                                )
        self.boss = Spaceship("assets/boss.png",
                              10,
                              -BOSS_SIZE,
                              HP_max=random.randrange(1000,10000),
                              velocity=1
                              )
        # Var declaration
        self.running = True
        self.score = 0
        self.last_spawn_ennemy = 0
        self.fps = pygame.time.Clock()
        self.font = pygame.font.Font(None,20)
        self.pause = False
        self.spawn_boss = False
        self.next_stage = 2000

    def run_menu(self):
        self.runing_menu = True
        while self.runing_menu:
            for evt in pygame.event.get():
                if evt.type == pygame.QUIT:
                    self.runing_menu = False
                if evt.type == pygame.MOUSEBUTTONDOWN:
                    abs_offset = self.menu_surface.get_abs_offset()
                    relative_x = evt.pos[0] - abs_offset[0]
                    relative_y = evt.pos[1] - abs_offset[1]
                    if self.start_button.rect.collidepoint(relative_x, relative_y):
                        self.run()
                    if self.exit_button.rect.collidepoint(relative_x, relative_y):
                        self.runing_menu = False                    
            
            self.menu_surface.fill(BG_MENU)
            self.game_surface.fill(BG_GAME)
        
            self.menu_surface.blit(self.start_button.surface, self.start_button.rect)
            self.menu_surface.blit(self.exit_button.surface, self.exit_button.rect)

            self.game_surface.blit(self.player.img, self.player.rect)

            pygame.display.flip()
            

    def handle_event(self) -> None:
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                self.running = False
                self.runing_menu = False
            
            if evt.type == pygame.MOUSEBUTTONDOWN:
                    abs_offset = self.menu_surface.get_abs_offset()
                    relative_x = evt.pos[0] - abs_offset[0]
                    relative_y = evt.pos[1] - abs_offset[1]
                    if self.exit_button.rect.collidepoint(relative_x, relative_y):
                        self.running = False
                        self.runing_menu = False

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
        if not self.spawn_boss:
            if pygame.time.get_ticks() - self.last_spawn_ennemy >= 500:
                self.ennemy_spawn()
                self.last_spawn_ennemy = pygame.time.get_ticks()
        else:
            if self.boss.rect.y < 10:
                self.boss.move_down()

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
                continue
            
            # manage collision torpedo and ennemys
            for ennemy in self.ennemys:
                if ennemy.rect.colliderect(elt.rect):
                    ennemy.HP -= elt.damage
                    elt.piercing -= 1

                    if ennemy.HP <= 0:
                        self.ennemys.remove(ennemy)
                        self.score += 100
            
            if elt.piercing <= 0:
                self.player.torpedo.remove(elt)
                continue
            
            # manage collision torpedo and boss
            if self.boss.rect.colliderect(elt.rect):
                self.boss.HP -= elt.damage
                elt.piercing -= 1
            
            if elt.piercing <= 0:
                self.player.torpedo.remove(elt)
                continue

        # verify player life
        if self.player.HP <= 0:
            self.running = False
            print(self.score)
            print("End")
        else:
            # Boss death
            if self.boss.HP <= 0:
                # set ennemy spawn 
                self.spawn_boss = False
                # delete the object from the screen
                self.boss.display = False
                self.boss.collable_allowed = False
                self.boss.set_pos(10, -BOSS_SIZE)
            
            # Boss appearance
            if self.score >= self.next_stage:
                # Create a new object Spaceship for the Boss
                self.boss = Spaceship("assets/boss.png",
                                      10,
                                      -BOSS_SIZE,
                                      HP_max=random.randrange(1000,10000),
                                      velocity=1
                                      )
                # booleen to stop ennemys spawn
                self.spawn_boss = True
                # set the next stage for the next boss
                self.next_stage += self.next_stage

    def display(self) -> None:
        
        # game surface update
        self.game_surface.fill(BG_GAME)
        
        for elt in self.player.torpedo:
            self.game_surface.blit(elt.img, elt.rect)
        
        for elt in self.ennemys:
            self.game_surface.blit(elt.img, elt.rect)
        
        self.game_surface.blit(self.player.img, self.player.rect)
        if self.boss.display:
            self.game_surface.blit(self.boss.img, self.boss.rect)

        # menu surface update
        self.menu_surface.fill(BG_MENU)

        score_text = self.font.render(f"Score : {self.score}",True, BG_GAME)
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
        for i in range(random.randrange(4,6)):
            buffer_ennemy = Spaceship("assets/ennemy.png",
                                      random.randrange(0,GAME_WIDTH-SHIP_SIZE),
                                      -SHIP_SIZE
                                      )
            index = 0
            while index < len(self.ennemys):
                while buffer_ennemy.rect.colliderect(self.ennemys[index].rect):
                    buffer_ennemy = Spaceship("assets/ennemy.png",
                                              random.randrange(0,GAME_WIDTH-SHIP_SIZE),
                                              -SHIP_SIZE
                                              )
                    index = 0
                index += 1
            self.ennemys.append(buffer_ennemy)
