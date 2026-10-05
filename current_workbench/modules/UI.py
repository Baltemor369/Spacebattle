import pygame
import random
import sys
import json
from pathlib import Path
from modules.const import *
from typing import List
from modules.Spaceship import Spaceship
from modules.Label import Label
from modules.colors import RGB
from modules.Bonus import Bonus
from modules.Marketplace import Marketplace
from modules.Achievements import AchievementManager, ACHIEVEMENTS



# save file next to main.py, independent of the folder the game is launched from
SAVE_PATH = Path(__file__).resolve().parent.parent / "save.json"

# player's attributes kept in the save file
SAVED_SKILLS = ["HP_max", "velocity", "att_speed", "att_velocity", "damage", "piercing"]

# statistics kept over all games (used by the achievements)
START_STATS = {"kills": 0, "bosses": 0, "bonus": 0, "games": 0, "purchases": 0}

TOAST_TIME = 3000   # ms during which a notification is shown


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

        # surface for score, menu, and other
        self.menu_surface = screen.subsurface(pygame.Rect(GAME_WIDTH,
                                                          0,
                                                          SCREEN_WIDTH-GAME_WIDTH,
                                                          SCREEN_HEIGHT)
                                              )

        self.font = pygame.font.Font(None,20)
        self.title_font = pygame.font.Font(None,40)
        self.fps = pygame.time.Clock()

        # page shown on the game surface while in the menu: "main", "shop" or "achievements"
        self.menu_page = "main"
        self.toasts = []

        # caches: surfaces are only rebuilt when what they show changes
        self._skill_key = None
        self._stellor_key = None
        self._score_key = None
        self._page_key = None

        self.start_button = self.menu_button("Start", 20)
        self.shop_button = self.menu_button("Marche", self.menu_surface.get_height() - 250)
        self.achievements_button = self.menu_button("Succes", self.menu_surface.get_height() - 200)
        self.reset_button = self.menu_button("Reset", self.menu_surface.get_height() - 150)
        self.param_button = self.menu_button("param", self.menu_surface.get_height() - 100)
        self.exit_button = self.menu_button("Exit", self.menu_surface.get_height() - 20 - 30)

        self.reset_progress()
        self.load_progress()

        self.run_menu()

    def menu_button(self, txt:str, y:float) -> Label:
        """
        Creates a button centered on the menu surface.

        args:
            txt (str): text of the button.
            y (float): top position of the button.
        """
        width = 70
        return Label(root_surface=self.menu_surface,
                     txt=txt,
                     topleft=((self.menu_surface.get_width() - width) / 2, y),
                     size=(width,30),
                     padding=(10,10,10,10),
                     bg=RGB("gray"),
                     fg=RGB("black"),
                     border_color=RGB("black"),
                     border_size=2)

    def reset_progress(self):
        """ Resets the player's skills, Stellor, items, achievements and difficulty to start again from 0. """
        self.player = Spaceship(path="assets/spaceship.png",
                                coord=((GAME_WIDTH - SHIP_SIZE) / 2, GAME_HEIGHT - 100),
                                hp=PLAYER_HP,
                                velocity=PLAYER_VELOCITY,
                                att_speed=PLAYER_ATT_SPEED,
                                att_velocity=PLAYER_ATT_VELOCITY,
                                damage=PLAYER_DMG,
                                piercing=PLAYER_PIERCING,
                                invicible_time=PLAYER_INVICIBLE_TIME,
                                display=True)
        if self.player == -1:
            print("Error: player cannot be initialized")
            sys.exit()

        self.player_stellor = START_STELLOR
        self.difficuly = 1
        self.marketplace = Marketplace()
        self.achievements = AchievementManager()
        self.stats = dict(START_STATS)

        self.init_game()

    def save_progress(self) -> None:
        """ Writes the player's Stellor, upgrades, items, statistics and achievements in the save file. """
        data = {"stellor": self.player_stellor}
        for skill in SAVED_SKILLS:
            data[skill] = getattr(self.player, skill)
        data["shop"] = self.marketplace.to_dict()
        data["stats"] = self.stats
        data["achievements"] = self.achievements.to_list()

        try:
            SAVE_PATH.write_text(json.dumps(data, indent=4), encoding="utf-8")
        except OSError as error:
            print(f"Error: progress cannot be saved ({error})")

    def load_progress(self) -> None:
        """ Restores the player's progress from the save file, if there is one. """
        if not SAVE_PATH.exists():
            return

        try:
            data = json.loads(SAVE_PATH.read_text(encoding="utf-8"))
            stellor = int(data["stellor"])
            skills = {skill: data[skill] for skill in SAVED_SKILLS}
            # parts added later: optional, so older save files still work
            shop = data.get("shop", {})
            stats = {key: int(data.get("stats", {}).get(key, 0)) for key in START_STATS}
            unlocked = list(data.get("achievements", []))
        except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
            # broken save: keep the fresh start rather than crashing
            print(f"Error: save file cannot be read, starting from 0 ({error})")
            return

        self.player_stellor = stellor
        for skill, value in skills.items():
            setattr(self.player, skill, value)
        self.player.HP = self.player.HP_max
        self.marketplace.load(shop)
        self.stats = stats
        self.achievements.load(unlocked)

    def init_game(self):
        """ Initializes data for the game """


        # Var declaration
        self.running = True
        self.score = START_SCORE
        self.last_spawn_ennemy = 0
        self.last_ennemy_fire = 0
        self.pause = False
        self.game_over = False
        self.spawn_boss = False
        self.next_stage = 2000

        # current game statistics
        self.game_frames = 0
        self.no_hit = True

        # bonus
        self.bonus_list:List[Bonus] = []
        self.shield_end = 0
        self.triple_end = 0

        # Player object
        self.player.set_pos(((GAME_WIDTH - SHIP_SIZE) / 2, GAME_HEIGHT - 100))
        self.player.HP = self.player.HP_max
        self.player.collable = True
        self.player = Spaceship(self.player)
        self.player.torpedo = []
        if self.player == -1:
            print("Error: player cannot be initialized")
            sys.exit()

        # list of ennemy objects
        self.ennemys:List[Spaceship] = []

        # torpedos fired by ennemys (kept here so they survive their shooter)
        self.ennemy_torpedo = []

        # Boss object
        self.boss = Spaceship(path="assets/boss.png",
                              coord=(10, -BOSS_SIZE),
                              hp=self.next_stage,
                              velocity=1,
                              att_speed=BOSS_FIRE_SPEED,
                              att_velocity=5,
                              damage=BOSS_TORPEDO_DMG,
                              piercing=1,
                              invicible_time=50,
                              display=False)

        if self.boss == -1:
            print("Error: boss cannot be initialized")
            sys.exit()
        self.boss.torpedo = self.ennemy_torpedo

        self.boss_life_bar = Label(root_surface=self.game_surface,
                                   txt="",
                                   topleft=(5,5),
                                   size=(0,0),
                                   bg=(255,0,0),
                                   fg=(220,0,0),
                                   border_color=(210,0,0),
                                   border_size=1,
                                   display=False)

# -------------------- Notifications & achievements --------------------#

    def notify(self, txt:str, color:tuple[int,int,int]=(255, 215, 0)) -> None:
        """
        Shows a short message at the top of the game surface.

        args:
            txt (str): the message.
            color (tuple): color of the text.
        """
        surface = self.font.render(txt, True, color)
        box = pygame.Surface((surface.get_width() + 16, surface.get_height() + 10), pygame.SRCALPHA)
        box.fill((0, 0, 0, 190))
        box.blit(surface, (8, 5))
        self.toasts.append((box, pygame.time.get_ticks() + TOAST_TIME))

    def draw_toasts(self) -> None:
        """ Draws the notifications still active on the game surface. """
        now = pygame.time.get_ticks()
        # only the 3 most recent ones, so they never cover the whole screen
        self.toasts = [toast for toast in self.toasts if toast[1] > now][-3:]
        y = 80
        for box, end in self.toasts:
            self.game_surface.blit(box, box.get_rect(midtop=(GAME_WIDTH / 2, y)))
            y += box.get_height() + 4

    def check_achievements(self) -> None:
        """ Unlocks the achievements whose condition is met and gives their reward. """
        stats = dict(self.stats)
        stats.update(score=self.score,
                     game_time=self.game_frames / FPS,
                     no_hit=self.no_hit,
                     att_speed=self.player.att_speed)

        new = self.achievements.check(stats)
        for achievement in new:
            self.player_stellor += achievement.reward
            self.notify(f"Succes : {achievement.name}  (+{achievement.reward} Stellor)")
        if new:
            self.save_progress()

# -------------------- Menu Loop --------------------#

    def run_menu(self):
        self.runing_menu = True
        while self.runing_menu:

            self.menu_events()

            self.menu_display()

            pygame.display.flip()
            self.fps.tick(30)

    def menu_events(self):
        for evt in pygame.event.get():

            if evt.type == pygame.QUIT:
                self.runing_menu = False

            elif evt.type == pygame.KEYDOWN:
                self.keypress_manager(evt)

            elif evt.type == pygame.MOUSEBUTTONDOWN:
                self.click_manager(evt)

    def keypress_manager(self, evt:pygame.event.Event):
        """
        Keypress manager

        args:
            evt (pygame.event.Event): Event object from pygame
        """
        if evt.key == pygame.K_ESCAPE:
            # Esc closes the shop / achievements page first, then the game
            if self.menu_page != "main":
                self.menu_page = "main"
            else:
                self.runing_menu = False

    def click_manager(self, evt:pygame.event.Event):
        """
        Click manager

        args:
            evt (pygame.event.Event): Event object from pygame
        """
        # click on the game surface: shop page buttons
        if self.game_surface.get_rect().collidepoint(evt.pos):
            if self.menu_page == "shop":
                self.shop_click(evt.pos)
            return

        abs_offset = self.menu_surface.get_abs_offset()
        relative_x = evt.pos[0] - abs_offset[0]
        relative_y = evt.pos[1] - abs_offset[1]

        if self.start_button.rect.collidepoint(relative_x, relative_y):
            self.menu_page = "main"
            self.run()

        elif self.shop_button.rect.collidepoint(relative_x, relative_y):
            self.menu_page = "main" if self.menu_page == "shop" else "shop"

        elif self.achievements_button.rect.collidepoint(relative_x, relative_y):
            self.menu_page = "main" if self.menu_page == "achievements" else "achievements"

        elif self.reset_button.rect.collidepoint(relative_x, relative_y):
            self.reset_progress()
            self.save_progress()

        elif self.exit_button.rect.collidepoint(relative_x, relative_y):
            self.runing_menu = False

        else:
            self.skill_click(relative_x, relative_y)

    def skill_click(self, x:float, y:float) -> None:
        """
        Buys the upgrade whose "+" button is at (x, y) if the player has enough Stellor.

        args:
            x (float): x position of the click on the menu surface.
            y (float): y position of the click on the menu surface.
        """
        upgrades = [(self.HP_up_B, self.lvl_hp, self.player.HP_upgrade, True),
                    (self.velocity_up_B, self.lvl_velocity, self.player.velocity_upgrade, True),
                    (self.att_speed_up_B, self.lvl_att_speed, self.player.att_speed_upgrade,
                     self.player.att_speed > PLAYER_MIN_ATT_SPEED),
                    (self.att_velo_up_B, self.lvl_att_velocity, self.player.att_velo_upgrade, True),
                    (self.att_up_B, self.lvl_damage, self.player.damage_upgrade, True),
                    (self.piercing_up_B, self.lvl_piercing, self.player.piercing_upgrade, True)]

        for button, lvl, upgrade, available in upgrades:
            if button.rect.collidepoint(x, y):
                cost = lvl * UPGRADE_COST
                if available and self.player_stellor >= cost:
                    self.player_stellor -= cost
                    upgrade()
                    self.save_progress()
                return

    def shop_click(self, pos:tuple[int,int]) -> None:
        """
        Buys the Marketplace item whose button is at pos.

        args:
            pos (tuple): position of the click on the game surface.
        """
        for item, rect in self.shop_buttons:
            if rect.collidepoint(pos):
                price = self.marketplace.buy(item, self.player_stellor)
                if price:
                    self.player_stellor -= price
                    self.stats["purchases"] += 1
                    self.notify(f"Achete : {item.name}", (120, 230, 120))
                    self.save_progress()
                    self.check_achievements()
                return

    def menu_display(self):
        self.menu_surface.fill(RGB("white"))

        self.start_button.draw()

        # Stellor label, rebuilt only when the amount changes
        if self._stellor_key != self.player_stellor:
            self._stellor_key = self.player_stellor
            self.stellor_label = Label(root_surface=self.menu_surface,
                                       topleft=(5,60),
                                       txt=f"Stellor : {self.player_stellor}\nStellor = Galactic currency",
                                       fg=RGB("black"),
                                       border_color=RGB("white"),
                                       border_size=1,
                                       padding=(5,5,5,5))
        self.stellor_label.draw()

        self.skill_menu()

        self.shop_button.draw()
        self.achievements_button.draw()
        self.reset_button.draw()
        self.param_button.draw()
        self.exit_button.draw()

        # game surface: ship, marketplace or achievements
        if self.menu_page == "shop":
            self.shop_page()
        elif self.menu_page == "achievements":
            self.achievements_page()
        else:
            self.game_surface.fill(RGB("dark navy"))
            self.game_surface.blit(self.player.img, self.player.rect)

        self.draw_toasts()

    def page_title(self, surface:pygame.Surface, title:str) -> None:
        """ Draws the title of a menu page on its surface. """
        txt = self.title_font.render(title, True, (255, 255, 255))
        surface.blit(txt, txt.get_rect(midtop=(GAME_WIDTH / 2, 20)))
        hint = self.font.render("Echap ou re-clic sur le bouton pour fermer", True, (150, 150, 170))
        surface.blit(hint, hint.get_rect(midtop=(GAME_WIDTH / 2, 55)))

    def shop_page(self) -> None:
        """ Draws the Marketplace on the game surface (rebuilt only when Stellor or items change). """
        key = ("shop", self.player_stellor, tuple(self.marketplace.owned.values()))
        if self._page_key != key:
            self._page_key = key
            page = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
            page.fill(RGB("dark navy"))
            self.page_title(page, "MARCHE")

            self.shop_buttons = []
            y = 90
            for item in Marketplace.ITEMS:
                card = pygame.Rect(15, y, GAME_WIDTH - 30, 95)
                pygame.draw.rect(page, (25, 25, 60), card, border_radius=6)
                pygame.draw.rect(page, (90, 90, 140), card, 1, border_radius=6)

                level = self.marketplace.level(item.key)
                count = f"Stock {level}/{item.max_level}" if item.consumable else f"Niveau {level}/{item.max_level}"
                kind = "Consommable" if item.consumable else "Permanent"
                page.blit(self.font.render(item.name, True, (255, 255, 255)), (card.x + 12, card.y + 12))
                page.blit(self.font.render(item.description, True, (190, 190, 210)), (card.x + 12, card.y + 38))
                page.blit(self.font.render(f"{kind} - {count}", True, (150, 150, 180)), (card.x + 12, card.y + 64))

                # buy button: green if affordable, gray otherwise
                button = pygame.Rect(card.right - 130, card.y + 30, 115, 34)
                if self.marketplace.is_maxed(item):
                    label, color = "MAX", (70, 70, 70)
                else:
                    price = self.marketplace.price(item)
                    label = f"{price} Stellor"
                    color = (40, 150, 70) if self.player_stellor >= price else (90, 90, 90)
                pygame.draw.rect(page, color, button, border_radius=5)
                txt = self.font.render(label, True, (255, 255, 255))
                page.blit(txt, txt.get_rect(center=button.center))
                self.shop_buttons.append((item, button))

                y += 110
            self.page_surface = page

        self.game_surface.blit(self.page_surface, (0, 0))

    def achievements_page(self) -> None:
        """ Draws the achievements list on the game surface (rebuilt only when one is unlocked). """
        key = ("achievements", tuple(self.achievements.to_list()))
        if self._page_key != key:
            self._page_key = key
            page = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
            page.fill(RGB("dark navy"))
            self.page_title(page, f"SUCCES  {len(self.achievements.unlocked)}/{len(ACHIEVEMENTS)}")

            y = 85
            for achievement in ACHIEVEMENTS:
                done = achievement.key in self.achievements.unlocked
                card = pygame.Rect(15, y, GAME_WIDTH - 30, 50)
                pygame.draw.rect(page, (30, 70, 40) if done else (30, 30, 50), card, border_radius=6)

                mark = "[OK]" if done else "[  ]"
                name_color = (130, 240, 130) if done else (200, 200, 200)
                page.blit(self.font.render(f"{mark} {achievement.name}", True, name_color), (card.x + 10, card.y + 8))
                page.blit(self.font.render(achievement.description, True, (170, 170, 190)), (card.x + 10, card.y + 28))
                reward = self.font.render(f"+{achievement.reward} Stellor", True, (255, 215, 0))
                page.blit(reward, reward.get_rect(midright=(card.right - 10, card.centery)))
                y += 56
            self.page_surface = page

        self.game_surface.blit(self.page_surface, (0, 0))

# -------------------- Game Loop --------------------#

    def handle_event(self) -> None:
        for evt in pygame.event.get():

            if evt.type == pygame.QUIT:
                self.running = False
                self.runing_menu = False

            elif evt.type == pygame.MOUSEBUTTONDOWN:
                abs_offset = self.menu_surface.get_abs_offset()
                relative_x = evt.pos[0] - abs_offset[0]
                relative_y = evt.pos[1] - abs_offset[1]

                if self.exit_button.rect.collidepoint(relative_x, relative_y):
                    self.running = False
                else:
                    self.skill_click(relative_x, relative_y)

            elif evt.type == pygame.KEYDOWN:

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
                spread = 3 if pygame.time.get_ticks() < self.triple_end else 1
                self.player.fire("up", spread=spread)

    def update(self) -> None:
        self.game_frames += 1

        # Boss phase init
        if self.score >= self.next_stage:
            self.init_boss_phase()

        #  ennemy phase
        if not self.boss.display:
            # generation of ennemys: waves get closer and bigger with the score
            spawn_delay = max(600, 1400 - self.score // 5)
            if pygame.time.get_ticks() - self.last_spawn_ennemy >= spawn_delay:
                self.ennemy_spawn(random.randrange(2, 4) + min(3, self.score // 1500))
                self.last_spawn_ennemy = pygame.time.get_ticks()

            # ennemy fire
            fire_delay = max(600, 1500 - self.score // 4)
            if self.ennemys and pygame.time.get_ticks() - self.last_ennemy_fire >= fire_delay:
                random.choice(self.ennemys).fire("down")
                self.last_ennemy_fire = pygame.time.get_ticks()

        # boss phase
        else:
            if pygame.time.get_ticks() - self.boss.last_collision >= self.boss.invicible_time:
                self.boss.collable = True

            # boss move
            if self.boss.rect.y < 10:
                self.boss.move_down()

            # boss fire (somewhere along its width, once arrived)
            else:
                self.boss.fire("down", random.randrange(self.boss.rect.x, self.boss.rect.right - TORPEDO_SIZE))

        # ennemy management
        self.manage_ennemys()

        # torpedo management
        self.player.manage_torpedo()
        Spaceship.manage_torpedo_list(self.ennemy_torpedo)

        # bonus management
        self.manage_bonus()

        # player invincibility end
        if pygame.time.get_ticks() - self.player.last_collision >= self.player.invicible_time:
            self.player.collable = True

        # collisions
        self.handle_collision()

        # player death
        if self.player.HP == 0:
            if self.marketplace.use("second_chance"):
                # item from the Marketplace: back with half HP and a moment of invincibility
                self.player.HP = self.player.HP_max // 2
                self.player.collable = False
                self.player.last_collision = pygame.time.get_ticks()
                self.notify("Seconde chance !", (120, 230, 120))
                self.save_progress()
            else:
                self.running = False
                self.game_over = True

        else:
            # Boss death
            if self.boss.HP == 0:
                # reset properties of self.boss
                self.boss.display = False
                self.boss.HP = self.next_stage
                self.boss.set_pos((10, -BOSS_SIZE))
                self.stats["bosses"] += 1

                # pts earned = 20 % boss' HP_max : 2000 HP <=> 400 pts
                self.score += int(self.boss.HP_max * 0.2)

        # achievements (no need to check them at each frame)
        if self.game_frames % 30 == 0:
            self.check_achievements()

    def player_hit(self, damage:int) -> None:
        """
        Applies damage to the player, unless the shield bonus is active.

        args:
            damage (int): amount of damage.
        """
        if pygame.time.get_ticks() < self.shield_end:
            return
        self.player.take_damage(damage)
        self.no_hit = False

    def manage_ennemys(self):
        for elt in self.ennemys[:]:
            elt.move_down()

            # out map
            if elt.rect.y >= GAME_HEIGHT+SHIP_SIZE:
                self.ennemys.remove(elt)
                continue

            # manage collision player-ennemys: the ennemy explodes on the player
            if self.player.rect.colliderect(elt.rect) and self.player.collable:
                self.player_hit(ENNEMY_COLLISION_DMG)
                self.ennemys.remove(elt)

    def manage_bonus(self):
        """ Moves the bonus, removes the ones out of map and applies the ones picked up. """
        for bonus in self.bonus_list[:]:
            bonus.move()

            if bonus.rect.y >= GAME_HEIGHT:
                self.bonus_list.remove(bonus)

            elif bonus.rect.colliderect(self.player.rect):
                self.bonus_list.remove(bonus)
                self.apply_bonus(bonus.kind)

    def apply_bonus(self, kind:str) -> None:
        """
        Applies the effect of a bonus picked up by the player.

        args:
            kind (str): type of the bonus.
        """
        now = pygame.time.get_ticks()
        duration = BONUS_DURATION + 2000 * self.marketplace.level("bonus_time")

        if kind == "heal":
            self.player.HP = min(self.player.HP_max, self.player.HP + BONUS_HEAL)
        elif kind == "triple":
            self.triple_end = max(self.triple_end, now) + duration
        elif kind == "shield":
            self.shield_end = max(self.shield_end, now) + duration

        self.stats["bonus"] += 1
        self.notify(Bonus.name(kind), (255, 255, 255))

    def drop_bonus(self, ennemy:Spaceship) -> None:
        """
        Sometimes drops a bonus where an ennemy was destroyed.

        args:
            ennemy (Spaceship): the destroyed ennemy.
        """
        chance = BONUS_DROP_CHANCE + 0.04 * self.marketplace.level("magnet")
        if random.random() < chance:
            self.bonus_list.append(Bonus(Bonus.random_kind(), ennemy.rect.center))

    def handle_collision(self):
        # manage player's torpedo collision
        for torpedo in self.player.torpedo:
            # collision torpedo & ennemys (iterate on a copy: dead ennemys are removed)
            for ennemy in self.ennemys[:]:
                if torpedo.piercing <= 0:
                    break

                if ennemy.rect.colliderect(torpedo.rect) and ennemy.collable and torpedo.collable:
                    ennemy.take_damage(torpedo.damage)
                    torpedo.collision()

                    # ennemy death
                    if ennemy.HP == 0:
                        self.ennemys.remove(ennemy)
                        self.score += random.randrange(75,125)
                        self.stats["kills"] += 1
                        self.drop_bonus(ennemy)

            # collision torpedo & boss (only when the boss is on screen)
            if self.boss.display and torpedo.piercing > 0 and self.boss.rect.colliderect(torpedo.rect):
                self.boss.take_damage(torpedo.damage)
                self.boss_life_bar.resize((self.boss.HP * (GAME_WIDTH - 10)) / self.boss.HP_max, 10)
                torpedo.collision()

        # collision player & boss
        if (self.boss.display and self.boss.rect.colliderect(self.player.rect)
                and self.boss.collable and self.player.collable):
            self.boss.take_damage(self.player.damage)
            self.player_hit(BOSS_COLLISION_DMG)

        # collision player & ennemys' torpedo
        for torp in self.ennemy_torpedo:
            if self.player.rect.colliderect(torp.rect) and self.player.collable and torp.collable and torp.piercing > 0:
                self.player_hit(torp.damage)
                torp.collision()

    def init_boss_phase(self):
        # set new boss appearence
        self.boss.display = True

        # boss stat update
        self.boss.HP_max = self.next_stage
        self.boss.HP = self.boss.HP_max

        # boss life bar update
        self.boss_life_bar.display = True
        self.boss_life_bar.resize((self.boss.HP * (GAME_WIDTH - 10)) / self.boss.HP_max, 10)

        # set the next stage for the next boss
        self.next_stage *= 2

    def display(self, flip:bool=True) -> None:
        now = pygame.time.get_ticks()

        # game surface update
        self.game_surface.fill(RGB("dark navy"))

        # player display (blinks while invincible after a hit)
        blink_hidden = not self.player.collable and (now // 100) % 2 == 0
        if self.player.display and not blink_hidden:
            self.game_surface.blit(self.player.img, self.player.rect)

        # shield bonus around the player
        if now < self.shield_end:
            pygame.draw.circle(self.game_surface, (80, 200, 255), self.player.rect.center, SHIP_SIZE * 0.85, 2)

        # torpedos' player display
        for elt in self.player.torpedo:
            if elt.display:
                self.game_surface.blit(elt.img, elt.rect)

        # ennemys display
        for elt in self.ennemys:
            if elt.display:
                self.game_surface.blit(elt.img, elt.rect)

        # ennemys' torpedo display
        for torpedo in self.ennemy_torpedo:
            if torpedo.display:
                self.game_surface.blit(torpedo.img, torpedo.rect)

        # bonus display
        for bonus in self.bonus_list:
            self.game_surface.blit(bonus.img, bonus.rect)

        # boss display
        if self.boss.display:
            self.game_surface.blit(self.boss.img, self.boss.rect)
            self.game_surface.blit(self.boss_life_bar.surface, self.boss_life_bar.rect)

        # player life bar
        self.player_life_bar()

        self.draw_toasts()

        # menu surface update
        self.menu_surface.fill(RGB("white"))

        # score text, rendered only when the score changes
        if self._score_key != self.score:
            self._score_key = self.score
            self.score_text = self.font.render(f"debris : {self.score}",True, RGB("black"))
        self.menu_surface.blit(self.score_text,((MENU_WIDTH-self.score_text.get_width())/2,10))

        # active bonus timers
        y = 35
        for name, end in (("Tir triple", self.triple_end), ("Bouclier", self.shield_end)):
            if now < end:
                txt = self.font.render(f"{name} : {(end - now) // 1000 + 1} s", True, (30, 110, 200))
                self.menu_surface.blit(txt, ((MENU_WIDTH - txt.get_width()) / 2, y))
                y += 20

        self.skill_menu()

        self.exit_button.draw()

        if flip:
            pygame.display.flip()

    def player_life_bar(self):
        """ Draws the player's life bar at the bottom of the game surface. """
        bar = pygame.Rect(5, GAME_HEIGHT - 20, GAME_WIDTH - 10, 14)
        ratio = self.player.HP / self.player.HP_max

        # green > 50 %, orange > 25 %, red under
        if ratio > 0.5:
            color = (40, 200, 60)
        elif ratio > 0.25:
            color = (240, 150, 20)
        else:
            color = (220, 30, 30)

        pygame.draw.rect(self.game_surface, (60, 60, 60), bar)
        pygame.draw.rect(self.game_surface, color, (bar.x, bar.y, int(bar.w * ratio), bar.h))
        pygame.draw.rect(self.game_surface, (255, 255, 255), bar, 1)

        hp_text = self.font.render(f"HP {self.player.HP} / {self.player.HP_max}", True, (255, 255, 255))
        self.game_surface.blit(hp_text, hp_text.get_rect(center=bar.center))

    def run(self):
        self.init_game()

        # items from the Marketplace used at the start of the game
        if self.marketplace.use("start_shield"):
            self.shield_end = pygame.time.get_ticks() + 5000
            self.notify("Bouclier de depart", (80, 200, 255))

        while self.running:
            self.handle_event()

            if self.pause:
                self.draw_overlay("PAUSE", "Echap pour reprendre")
                pygame.time.wait(100)

            else:
                self.update()

                self.display()

                self.fps.tick(FPS)

        earned = self.score // 2
        self.player_stellor += earned
        self.stats["games"] += 1
        self.check_achievements()
        self.save_progress()

        if self.game_over:
            self.game_over_screen(earned)

    def draw_overlay(self, title:str, subtitle:str) -> None:
        """
        Draws a darkened screen over the game with a title and a subtitle.

        args:
            title (str): big text in the middle of the game surface.
            subtitle (str): smaller text under the title, one line per "\\n".
        """
        self.display(flip=False)
        shade = pygame.Surface((GAME_WIDTH, GAME_HEIGHT), pygame.SRCALPHA)
        shade.fill((0, 0, 0, 160))
        self.game_surface.blit(shade, (0, 0))

        big_font = pygame.font.Font(None, 60)
        title_txt = big_font.render(title, True, (255, 255, 255))
        y = GAME_HEIGHT / 2 - 60
        self.game_surface.blit(title_txt, title_txt.get_rect(center=(GAME_WIDTH / 2, y)))

        for line in subtitle.split("\n"):
            y += 35
            line_txt = self.font.render(line, True, (220, 220, 220))
            self.game_surface.blit(line_txt, line_txt.get_rect(center=(GAME_WIDTH / 2, y)))

        pygame.display.flip()

    def game_over_screen(self, earned:int) -> None:
        """
        Shows the end of game screen until the player clicks or presses a key.

        args:
            earned (int): Stellor earned during the game.
        """
        self.draw_overlay("GAME OVER",
                          f"Debris : {self.score}\n+{earned} Stellor\nClique ou appuie sur une touche")
        pygame.time.wait(500)   # avoid skipping the screen with a key still pressed
        pygame.event.clear()

        while True:
            evt = pygame.event.wait()
            if evt.type == pygame.QUIT:
                self.runing_menu = False
                return
            if evt.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                return

    def ennemy_spawn(self, count:int):
        """
        Spawns a wave of ennemys at the top of the game surface, without overlapping.

        args:
            count (int): number of ennemys in the wave.
        """
        for i in range(count):
            # try a few random places, give up if the top of the map is too crowded
            for attempt in range(20):
                coord = (random.randrange(0, GAME_WIDTH - SHIP_SIZE), -SHIP_SIZE)
                spot = pygame.Rect(coord, (SHIP_SIZE, SHIP_SIZE))
                if not any(spot.colliderect(elt.rect) for elt in self.ennemys):
                    break
            else:
                continue

            ennemy = Spaceship(path="assets/ennemy.png",
                               coord=coord,
                               hp=ENNEMY_HP,
                               velocity=ENNEMY_VELOCITY,
                               att_speed=1000,
                               att_velocity=5,
                               damage=ENNEMY_TORPEDO_DMG,
                               piercing=1,
                               invicible_time=0,
                               display=True)
            ennemy.torpedo = self.ennemy_torpedo
            self.ennemys.append(ennemy)

    def skill_menu(self):
        """ Draws the skills and their "+" buttons, rebuilt only when a skill changes. """
        key = tuple(getattr(self.player, skill) for skill in SAVED_SKILLS)
        if self._skill_key != key:
            self._skill_key = key
            self.build_skill_menu()

        for label in self.skill_labels:
            label.draw()

    def build_skill_menu(self):
        """ Creates the labels and "+" buttons of the skills menu. """
        button_x = MENU_WIDTH - 30
        button_y = 120
        label_x = 20

        # skills div
        self.lvl_hp = (self.player.HP_max - PLAYER_HP) // Spaceship.HP_bonus + 1
        HP_label = Label(root_surface=self.menu_surface,
                         txt=f"{self.player.HP_max} HP max, lvl {self.lvl_hp}\n{self.lvl_hp * UPGRADE_COST} Stellor",
                         topleft=(label_x,button_y),
                         border_color=None)

        self.HP_up_B = Label(root_surface=self.menu_surface,
                           topleft=(button_x,button_y),
                           txt="+",
                           padding=(5,5,5,5),
                           bg=RGB("gray"),
                           fg=RGB("black"))

        button_y += 50
        self.lvl_velocity = (self.player.velocity - PLAYER_VELOCITY) // Spaceship.velocity_bonus + 1
        velocity_label = Label(root_surface=self.menu_surface,
                            topleft=(label_x, button_y),
                            txt=f"{self.player.velocity} Speed, lvl {self.lvl_velocity}\n{self.lvl_velocity * UPGRADE_COST} Stellor",
                          border_color=None)

        self.velocity_up_B = Label(root_surface=self.menu_surface,
                           topleft=(button_x,button_y),
                           txt="+",
                           padding=(5,5,5,5),
                           bg=RGB("gray"),
                           fg=RGB("black"))

        button_y += 50
        self.lvl_att_speed = (PLAYER_ATT_SPEED - self.player.att_speed) // Spaceship.att_speed_bonus + 1
        if self.player.att_speed > PLAYER_MIN_ATT_SPEED:
            att_speed_cost = f"{self.lvl_att_speed * UPGRADE_COST} Stellor"
        else:
            att_speed_cost = "MAX"
        att_speed_label = Label(root_surface=self.menu_surface,
                                topleft=(label_x, button_y),
                                txt=f"{self.player.att_speed} Speed Att, lvl {self.lvl_att_speed}\n{att_speed_cost}",
                                border_color=None)

        self.att_speed_up_B = Label(root_surface=self.menu_surface,
                                    topleft=(button_x,button_y),
                                    txt="+",
                                    padding=(5,5,5,5),
                                    bg=RGB("gray"),
                                    fg=RGB("black"))

        button_y += 50
        self.lvl_att_velocity = (self.player.att_velocity - PLAYER_ATT_VELOCITY) // Spaceship.att_velocity_bonus + 1
        att_velocity_label = Label(root_surface=self.menu_surface,
                               topleft=(label_x, button_y),
                               txt=f"{self.player.att_velocity} Velocity Att, lvl {self.lvl_att_velocity}\n{self.lvl_att_velocity * UPGRADE_COST} Stellor",
                               border_color=None)

        self.att_velo_up_B = Label(root_surface=self.menu_surface,
                           topleft=(button_x,button_y),
                           txt="+",
                           padding=(5,5,5,5),
                           bg=RGB("gray"),
                           fg=RGB("black"))

        button_y += 50
        self.lvl_damage = (self.player.damage - PLAYER_DMG) // Spaceship.damage_bonus + 1
        damage_label = Label(root_surface=self.menu_surface,
                          topleft=(label_x, button_y),
                          txt=f"{self.player.damage} Damage, lvl {self.lvl_damage}\n{self.lvl_damage * UPGRADE_COST} Stellor",
                          border_color=None)

        self.att_up_B = Label(root_surface=self.menu_surface,
                           topleft=(button_x,button_y),
                           txt="+",
                           padding=(5,5,5,5),
                           bg=RGB("gray"),
                           fg=RGB("black"))

        button_y += 50
        self.lvl_piercing = (self.player.piercing - PLAYER_PIERCING) // Spaceship.piercing_bonus + 1
        piercing_label = Label(root_surface=self.menu_surface,
                               topleft=(label_x, button_y),
                               txt=f"{self.player.piercing} Piercing, lvl {self.lvl_piercing}\n{self.lvl_piercing * UPGRADE_COST} Stellor",
                               border_color=None)

        self.piercing_up_B = Label(root_surface=self.menu_surface,
                           topleft=(button_x,button_y),
                           txt="+",
                           padding=(5,5,5,5),
                           bg=RGB("gray"),
                           fg=RGB("black"))

        self.skill_labels = [HP_label, velocity_label, att_speed_label, att_velocity_label, damage_label, piercing_label,
                             self.HP_up_B, self.velocity_up_B, self.att_speed_up_B, self.att_velo_up_B,
                             self.att_up_B, self.piercing_up_B]
