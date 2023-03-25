import pygame
import random 
from modules.Spaceship import *
from modules.Button import ButtonRect

SHIP_SIZE = 32
FPS = 90
TORPEDO_SIZE = 16
BOSS_SIZE = 480
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
GAME_WIDTH = SCREEN_WIDTH-100
GAME_HEIGHT = 800
BG_GAME = (0,0,50)
BG_MENU = (255,255,255)
LIFE_BAR = (220,0,0)

START_SCORE = 0
PLAYER_DMG = 100

class Spacebattle:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Spacebattle")
        
        icon_32x32 = pygame.image.load("assets/logo.png")
        pygame.display.set_icon(icon_32x32)

        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # surface for the game
        self.game_surface = screen.subsurface(pygame.Rect(0,0,GAME_WIDTH,GAME_HEIGHT))
        self.game_surface.fill(BG_GAME)

        # surface for score, menu, and other
        self.menu_surface = screen.subsurface(pygame.Rect(GAME_WIDTH,
                                                          0,
                                                          SCREEN_WIDTH-GAME_WIDTH,
                                                          SCREEN_HEIGHT
                                                          )
                                              )
        self.menu_surface.fill(BG_MENU)
        
        # button "start"
        self.start_button = ButtonRect(50, 30, (20, 20), "Start")
        # button "exit"
        self.exit_button = ButtonRect(50, 30, (20, SCREEN_HEIGHT-50), "Exit")

        self.player_debris = 0

        self.init_game()

        self.run_menu()
    
    def init_game(self):

        # Var declaration
        self.running = True
        self.score = START_SCORE
        self.last_spawn_ennemy = 0
        self.fps = pygame.time.Clock()
        self.font = pygame.font.Font(None,20)
        self.pause = False
        self.spawn_boss = False
        self.next_stage = 2000

        # Player object
        self.player = Spaceship(path="assets/spaceship.png",
                              pos=((GAME_WIDTH - SHIP_SIZE) / 2, GAME_HEIGHT - 100),
                              HP_max = self.next_stage,
                              velocity=3,
                              att_speed=1000,
                              att_velocity=8,
                              torpedo_dmg=PLAYER_DMG,
                              torpedo_piercing=1,
                              )

        # list of ennemy objects
        self.ennemys:List[Spaceship] = []
        
        self.boss = Spaceship("assets/boss.png",
                              (10, -BOSS_SIZE),
                              HP_max = self.next_stage,
                              velocity=1,
                              att_speed=100,
                              att_velocity=8,
                              torpedo_dmg=100,
                              torpedo_piercing=1,
                              display=False
                              )
        self.boss_life_bar = ButtonRect((self.boss.HP * (GAME_WIDTH - 10)) / self.boss.HP_max, 
                                        10,
                                        (5,5),
                                        "",
                                        bg=(255,0,0),
                                        fg=(220,0,0),
                                        border_color=(210,0,0),
                                        display=False
                                        )

# -------------------- Menu Loop --------------------#

    def run_menu(self):
        self.runing_menu = True
        while self.runing_menu:

            self.menu_events()
            
            self.menu_display()

            pygame.display.flip()

    def menu_events(self):
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

    def menu_display(self):
        self.menu_surface.fill(BG_MENU)
        self.game_surface.fill(BG_GAME)
    
        self.menu_surface.blit(self.start_button.surface, self.start_button.rect)
        self.menu_surface.blit(self.exit_button.surface, self.exit_button.rect)

        self.game_surface.blit(self.player.img, self.player.rect)

# -------------------- Game Loop --------------------#

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

        # Boss phase init
        if self.score >= self.next_stage:

            # set the next stage for the next boss
            self.boss.display = True

            self.boss_life_bar.display = True
            self.boss_life_bar.resize((self.boss.HP * (GAME_WIDTH - 10)) / self.boss.HP_max, 10)
            
            # boss stat update
            self.boss.HP_max = self.next_stage

            # set new boss appearence
            self.next_stage *= 2
            
        #  not boss phase
        if not self.boss.display:

            if pygame.time.get_ticks() - self.last_spawn_ennemy >= 500:
                self.ennemy_spawn()
                self.last_spawn_ennemy = pygame.time.get_ticks()

        # boss phase
        else:
            
            if self.boss.rect.y < 10:

                self.boss.move_down()
            
            # boss torpedo algo :

        # ennemy move management
        for elt in self.ennemys:
            elt.move_down()

            # out map
            if elt.rect.y >= GAME_HEIGHT+SHIP_SIZE:
                self.ennemys.remove(elt)
                continue
            
            # manage collision player-ennemys
            if self.player.rect.colliderect(elt.rect):
                self.player.take_damage(elt.HP_max)

        # torpedo move managements
        for elt in self.player.torpedo:
            elt.move()

            # out map
            if elt.rect.y <= -TORPEDO_SIZE:
                self.player.torpedo.remove(elt)
                continue
            
            # manage collision torpedo and ennemys
            for ennemy in self.ennemys:
                
                # collision
                if ennemy.rect.colliderect(elt.rect):
                    
                    # if missile can do damage
                    if elt.piercing > 0:
                        ennemy.take_damage(elt.damage)
                        elt.collision()

                    # ennemy death
                    if ennemy.HP == 0:
                        self.ennemys.remove(ennemy)
                        self.score += 1000# random.randrange(75,125)

                    # missile destroyed
                    if elt.piercing == 0:
                        break
            
            # missile destroyed
            if elt.piercing == 0:
                self.player.torpedo.remove(elt)
                continue

            # manage collision torpedo and boss
            if self.boss.rect.colliderect(elt.rect):
                self.boss.take_damage(elt.damage)
                self.boss_life_bar.resize((self.boss.HP * (GAME_WIDTH - 10)) / self.boss.HP_max, 10)
                elt.collision()
            
            # missile destroyed
            if elt.piercing <= 0:
                self.player.torpedo.remove(elt)
                continue

        # player death
        if self.player.HP == 0:
            self.running = False
            print(self.score)
            print("End")

        else:
            # Boss death
            if self.boss.HP == 0:
                # reset properties of self.boss
                self.boss.display = False
                self.boss.HP = self.next_stage
                self.boss.set_pos(10, -BOSS_SIZE)
                
                # pts earned = 20 % boss' HP_max : 2000 HP <=> 400 pts
                self.score += int(self.boss.HP_max * 0.1)

    def display(self) -> None:
        
        # game surface update
        self.game_surface.fill(BG_GAME)
        
        for elt in self.player.torpedo:
            if elt.display:
                self.game_surface.blit(elt.img, elt.rect)
        
        for elt in self.ennemys:
            if elt.display:
                self.game_surface.blit(elt.img, elt.rect)
        
        if self.player.display:
            self.game_surface.blit(self.player.img, self.player.rect)
        
        if self.boss.display:
            self.game_surface.blit(self.boss.img, self.boss.rect)
            self.game_surface.blit(self.boss_life_bar.surface, self.boss_life_bar.rect)

        # menu surface update
        self.menu_surface.fill(BG_MENU)

        score_text = self.font.render(f"debris : {self.score}",True, BG_GAME)
        self.menu_surface.blit(score_text,(10,10))

        self.menu_surface.blit(self.exit_button.surface, self.exit_button.rect)

        pygame.display.flip()

    def run(self):
        # self.init_game()

        while self.running:
            self.handle_event()
            
            if self.pause:
                pygame.time.wait(200)

            else:
                self.update()

                self.display()

                self.fps.tick(FPS)
    
    def ennemy_spawn(self):
        buffer_ennemy = Spaceship(path="assets/ennemy.png",
                              pos=(self.player.rect.x, -SHIP_SIZE),
                              HP_max = 100,
                              velocity=3,
                              att_speed=100,
                              att_velocity=8,
                              torpedo_dmg=100,
                              torpedo_piercing=1,
                              )
        
        for i in range(random.randrange(4,6)):
            
            buffer_ennemy = Spaceship("assets/ennemy.png",
                                  pos=(random.randrange(0,GAME_WIDTH-SHIP_SIZE), -SHIP_SIZE),
                                  HP_max=100,
                                  velocity=3,
                                  att_speed=100,
                                  att_velocity=8,
                                  torpedo_dmg=100,
                                  torpedo_piercing=1
                                  )
            
            index = 0
            while index < len(self.ennemys):
                while buffer_ennemy.rect.colliderect(self.ennemys[index].rect):
                    buffer_ennemy = Spaceship("assets/ennemy.png",
                                              pos=(random.randrange(0,GAME_WIDTH-SHIP_SIZE), -SHIP_SIZE),
                                              HP_max=100,
                                              velocity=3,
                                              att_speed=100,
                                              att_velocity=8,
                                              torpedo_dmg=100,
                                              torpedo_piercing=1
                                              )
                    index = 0
                index += 1
            self.ennemys.append(buffer_ennemy)
