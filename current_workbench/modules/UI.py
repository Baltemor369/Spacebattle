import pygame
import random 
from modules.Spaceship import *
from modules.Label import Label
from modules.colors import RGB

SHIP_SIZE = 32
FPS = 90
TORPEDO_SIZE = 16
BOSS_SIZE = 480

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 800

GAME_WIDTH = 500
GAME_HEIGHT = 800

MENU_WIDTH = 200
MENU_HEIGHT = 800

START_SCORE = 0
PLAYER_DMG = 100

class Spacebattle:
    def __init__(self) -> None:
        """
        Initialize the Spacebattle game.
        """
        pygame.init()
        pygame.display.set_caption("Spacebattle")
        
        icon_32x32 = pygame.image.load("assets/logo.png")
        pygame.display.set_icon(icon_32x32)

        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # surface for the game
        self.game_surface = screen.subsurface(pygame.Rect(0,0,GAME_WIDTH,GAME_HEIGHT))
        # self.game_surface.fill(RGB("dark navy"))

        # surface for score, menu, and other
        self.menu_surface = screen.subsurface(pygame.Rect(GAME_WIDTH,
                                                          0,
                                                          SCREEN_WIDTH-GAME_WIDTH,
                                                          SCREEN_HEIGHT
                                                          )
                                              )
        # self.menu_surface.fill(RGB("white"))
        
        # button "start"
        x = self.menu_surface.get_width() / 2 - 50 / 2
        y = 20
        self.start_button = Label(root_surface=self.menu_surface,
                                  txt="Start",
                                  topleft=(x,y),
                                  size=(50,30),
                                  padding=(10,10,10,10),
                                  bg=RGB("gray"),
                                  fg=RGB("black"),
                                  border_size=2)

        # button "param"
        x = self.menu_surface.get_width() / 2 - 50 / 2
        y = self.menu_surface.get_height() - 100
        self.param_button = Label(root_surface=self.menu_surface,
                                  txt="param",
                                  topleft=(x,y),
                                  size=(50,30),
                                  padding=(10,10,10,10),
                                  bg=RGB("gray"),
                                  fg=RGB("black"),
                                  border_size=2)

        # button "exit"
        x = self.menu_surface.get_width() / 2 - 50 / 2
        y = self.menu_surface.get_height() - 20 - 30 # 20 = padding 30 = height of the label
        self.exit_button = Label(root_surface=self.menu_surface,
                                 txt="Exit",
                                 topleft=(x,y),
                                 size=(50,30),
                                 padding=(10,10,10,10),
                                 fg=RGB("black"),
                                 bg=RGB("gray"),
                                 border_color=RGB("black"),
                                 border_size=2)

        self.player = Spaceship(["assets/spaceship.png",
                                ((GAME_WIDTH - SHIP_SIZE) / 2, GAME_HEIGHT - 100),
                                100,
                                2,
                                800,
                                8,
                                PLAYER_DMG,
                                1,
                                True]
                                )

        self.player_stellor = 0
        self.difficuly = 1

        self.init_game()

        self.run_menu()
    
    def init_game(self):
        """ Initializes data for the game """


        # Var declaration
        self.running = True
        self.score = START_SCORE
        self.last_spawn_ennemy = 0
        self.last_ennemy_fire = 0
        self.fps = pygame.time.Clock()
        self.font = pygame.font.Font(None,20)
        self.pause = False
        self.spawn_boss = False
        self.next_stage = 2000

        # Player object
        self.player.set_pos(((GAME_WIDTH - SHIP_SIZE) / 2, GAME_HEIGHT - 100))
        self.player.HP = self.player.HP_max
        self.player = Spaceship(self.player)

        # list of ennemy objects
        self.ennemys:List[Spaceship] = []
        
        self.boss = Spaceship(["assets/boss.png",
                              (10, -BOSS_SIZE),
                              self.next_stage,
                              1,
                              100,
                              8,
                              100,
                              1,
                              False]
                              )
        self.boss_life_bar = Label(root_surface=self.game_surface,
                                   txt="",
                                   topleft=(5,5),
                                   size=(0,0),
                                   bg=(255,0,0),
                                   fg=(220,0,0),
                                   border_color=(210,0,0),
                                   border_size=1,
                                   display=False)
        
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
                        self.running = False

                elif self.HP_up_B.rect.collidepoint(relative_x, relative_y):
                    self.player.HP_upgrade()

                elif self.velocity_up_B.rect.collidepoint(relative_x, relative_y):
                    self.player.velocity_upgrade()

                elif self.att_speed_up_B.rect.collidepoint(relative_x, relative_y):
                    self.player.att_speed_upgrade()

                elif self.att_velo_up_B.rect.collidepoint(relative_x, relative_y):
                    self.player.att_velo_upgrade()

                elif self.att_up_B.rect.collidepoint(relative_x, relative_y):
                    self.player.damage_upgrade()
                    
                elif self.piercing_up_B.rect.collidepoint(relative_x, relative_y):
                    self.player.piercing_upgrade()
                
                if self.exit_button.rect.collidepoint(relative_x, relative_y):
                    self.runing_menu = False

    def menu_display(self):
        self.menu_surface.fill(RGB("white"))
        self.game_surface.fill(RGB("dark navy"))
    
        self.menu_surface.blit(self.start_button.surface, self.start_button.rect)
        
        x = 5
        y = 60
        stellor = Label(root_surface=self.game_surface,
                        topleft=(x,y),
                        txt=f"Stellor : {self.player_stellor}\nStellor = Galactic currency",
                        fg=RGB("black"),
                        border_color=RGB("white"),
                        border_size=1,
                        padding=(5,5,5,5))
        self.menu_surface.blit(stellor.surface, stellor.rect)

        self.skill_menu(self.menu_surface)

        self.menu_surface.blit(self.param_button.surface, self.param_button.rect)

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

                    elif self.HP_up_B.rect.collidepoint(relative_x, relative_y):
                        self.player.HP_upgrade()

                    elif self.velocity_up_B.rect.collidepoint(relative_x, relative_y):
                        self.player.velocity_upgrade()

                    elif self.att_speed_up_B.rect.collidepoint(relative_x, relative_y):
                        self.player.att_speed_upgrade()

                    elif self.att_velo_up_B.rect.collidepoint(relative_x, relative_y):
                        self.player.att_velo_upgrade()

                    elif self.att_up_B.rect.collidepoint(relative_x, relative_y):
                        self.player.damage_upgrade()
                        
                    elif self.piercing_up_B.rect.collidepoint(relative_x, relative_y):
                        self.player.piercing_upgrade()


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
                self.player.fire("up")

    def update(self) -> None:

        # Boss phase init
        if self.score >= self.next_stage:

            # set the next stage for the next boss
            self.boss.display = True

            # boss life bar update
            self.boss_life_bar.display = True
            self.boss_life_bar.resize((self.boss.HP * (GAME_WIDTH - 10)) / self.boss.HP_max, 10)
            
            # boss stat update
            self.boss.HP_max = self.next_stage

            # set new boss appearence
            self.next_stage *= 2
            
        #  ennemy phase 
        if not self.boss.display:
            # generation of ennemys
            if pygame.time.get_ticks() - self.last_spawn_ennemy >= 500:
                self.ennemy_spawn()
                self.last_spawn_ennemy = pygame.time.get_ticks()
            
            # ennemy fire
            if pygame.time.get_ticks() - self.last_ennemy_fire >= 3000:
                self.ennemys[random.randrange(0,len(self.ennemys))].fire("down")

        # boss phase
        else:
            # boss move
            if self.boss.rect.y < 10:
                self.boss.move_down()

            # player & boss collision
            if self.boss.rect.colliderect(self.player.rect):
                self.running = False
            
            # boss fire

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
        self.player.manage_torpedo()
        for elt in self.player.torpedo:

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
                        self.score += random.randrange(75,125)

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
                self.boss.set_pos((10, -BOSS_SIZE))
                
                # pts earned = 20 % boss' HP_max : 2000 HP <=> 400 pts
                self.score += int(self.boss.HP_max * 0.1)

    def display(self) -> None:
        
        # game surface update
        self.game_surface.fill(RGB("dark navy"))
        
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
        self.menu_surface.fill(RGB("white"))

        score_text = self.font.render(f"debris : {self.score}",True, RGB("black"))
        self.menu_surface.blit(score_text,((MENU_WIDTH-score_text.get_width())/2,10))

        self.skill_menu(self.menu_surface)

        self.menu_surface.blit(self.exit_button.surface, self.exit_button.rect)

        pygame.display.flip()

    def run(self):
        self.init_game()

        while self.running:
            self.handle_event()
            
            if self.pause:
                pygame.time.wait(200)

            else:
                self.update()

                self.display()

                self.fps.tick(FPS)
        
        self.player_stellor += int(self.score / 2)
    
    def ennemy_spawn(self):
        buffer_ennemy = Spaceship(["assets/ennemy.png",
                              (self.player.rect.x, -SHIP_SIZE),
                               100,
                              3,
                              100,
                              5,
                              100,
                              1,
                              True]
                              )
        
        for i in range(random.randrange(4,6)):
            
            buffer_ennemy = Spaceship(["assets/ennemy.png",
                                  (random.randrange(0,GAME_WIDTH-SHIP_SIZE), -SHIP_SIZE),
                                  100,
                                  3,
                                  100,
                                  5,
                                  100,
                                  1,
                                  True]
                                  )
            
            index = 0
            while index < len(self.ennemys):
                while buffer_ennemy.rect.colliderect(self.ennemys[index].rect):
                    buffer_ennemy = Spaceship(["assets/ennemy.png",
                                            (random.randrange(0,GAME_WIDTH-SHIP_SIZE), -SHIP_SIZE),
                                            100,
                                            3,
                                            100,
                                            5,
                                            100,
                                            1,
                                            True]
                                            )
                    index = 0
                index += 1
            self.ennemys.append(buffer_ennemy)

    def skill_menu(self, surface:pygame.Surface):
        button_x = MENU_WIDTH - 30
        button_y = 120
        label_x = 40

        # skills div
        lvl = (self.player.HP_max - 100) // Spaceship.HP_bonus + 1
        HP_label = Label(root_surface=self.menu_surface,
                         txt=f"HP max, lvl {lvl}\n{lvl * 1000} Stellor",
                         topleft=(label_x,button_y),
                         border_color=None)
        
        self.HP_up_B = Label(root_surface=self.menu_surface,
                           topleft=(button_x,button_y),
                           txt="+",
                           padding=(5,5,5,5),
                           bg=RGB("gray"),
                           fg=RGB("black"))

        button_y += 50
        lvl = (self.player.velocity - 2) // Spaceship.velocity_bonus + 1
        velocity_label = Label(root_surface=self.menu_surface,
                            topleft=(label_x, button_y),
                            txt=f"Speed, lvl {lvl}\n{lvl * 1000} Stellor",
                          border_color=None)
        
        self.velocity_up_B = Label(root_surface=self.menu_surface,
                           topleft=(button_x,button_y),
                           txt="+",
                           padding=(5,5,5,5),
                           bg=RGB("gray"),
                           fg=RGB("black"))

        button_y += 50
        lvl = (self.player.att_speed - 800) // Spaceship.att_speed_bonus + 1
        att_speed_label = Label(root_surface=self.menu_surface,
                                topleft=(label_x, button_y),
                                txt=f"Speed Att, lvl {lvl}\n{lvl * 1000} Stellor",
                                border_color=None)
        
        self.att_speed_up_B = Label(root_surface=self.menu_surface,
                                    topleft=(button_x,button_y),
                                    txt="+",
                                    padding=(5,5,5,5),
                                    bg=RGB("gray"),
                                    fg=RGB("black"))

        button_y += 50
        lvl = (self.player.att_velocity - 8) // Spaceship.att_velocity_bonus + 1
        att_velo_label = Label(root_surface=self.menu_surface,
                               topleft=(label_x, button_y),
                               txt=f"Velocity Att, lvl {lvl}\n{lvl * 1000} Stellor",
                               border_color=None)
        
        self.att_velo_up_B = Label(root_surface=self.menu_surface,
                           topleft=(button_x,button_y),
                           txt="+",
                           padding=(5,5,5,5),
                           bg=RGB("gray"),
                           fg=RGB("black"))

        button_y += 50
        lvl = (self.player.damage - 100) // Spaceship.damage_bonus + 1
        att_label = Label(root_surface=self.menu_surface,
                          topleft=(label_x, button_y),
                          txt=f"Damage, lvl {lvl}\n{lvl * 1000} Stellor",
                          border_color=None)
        
        self.att_up_B = Label(root_surface=self.menu_surface,
                           topleft=(button_x,button_y),
                           txt="+",
                           padding=(5,5,5,5),
                           bg=RGB("gray"),
                           fg=RGB("black"))

        button_y += 50
        lvl = (self.player.piercing - 1) // Spaceship.piercing_bonus + 1
        piercing_label = Label(root_surface=self.menu_surface,
                               topleft=(label_x, button_y),
                               txt=f"Piercing, lvl {lvl}\n{lvl * 1000} Stellor",
                               border_color=None)
        
        self.piercing_up_B = Label(root_surface=self.menu_surface,
                           topleft=(button_x,button_y),
                           txt="+",
                           padding=(5,5,5,5),
                           bg=RGB("gray"),
                           fg=RGB("black"))

        HP_label.draw()
        velocity_label.draw()
        att_speed_label.draw()
        att_velo_label.draw()
        att_label.draw()
        piercing_label.draw()

        self.HP_up_B.draw()
        self.velocity_up_B.draw()
        self.att_speed_up_B.draw()
        self.att_velo_up_B.draw()
        self.att_up_B.draw()
        self.piercing_up_B.draw()