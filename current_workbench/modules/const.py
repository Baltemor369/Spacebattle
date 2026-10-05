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
START_STELLOR = 0
PLAYER_DMG = 100
# Player base stats
PLAYER_HP = 100
PLAYER_VELOCITY = 3
PLAYER_ATT_SPEED = 400          # ms between two shots
PLAYER_MIN_ATT_SPEED = 100      # att speed upgrades stop here
PLAYER_ATT_VELOCITY = 8
PLAYER_PIERCING = 1
PLAYER_INVICIBLE_TIME = 2000    # ms of invincibility after a hit

UPGRADE_COST = 500              # Stellor cost = level * UPGRADE_COST

# Ennemys
ENNEMY_HP = 100
ENNEMY_VELOCITY = 2
ENNEMY_TORPEDO_DMG = 20
ENNEMY_COLLISION_DMG = 35

# Boss
BOSS_FIRE_SPEED = 700           # ms between two boss shots
BOSS_TORPEDO_DMG = 25
BOSS_COLLISION_DMG = 50

# Bonus dropped by ennemys
BONUS_SIZE = 24
BONUS_VELOCITY = 2
BONUS_DROP_CHANCE = 0.10        # +4 % per "magnet" level bought in the Marketplace
BONUS_DURATION = 8000           # ms, +2 s per "bonus_time" level
BONUS_HEAL = 30
