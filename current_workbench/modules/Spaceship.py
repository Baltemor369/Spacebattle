
from typing import List
from pygame import time
import modules.Sprite as Sprite

TORPEDO_SIZE = 16


class Spaceship(Sprite.Sprite):
    # Basic stats
    HP_max = 100
    velocity = 4.0
    fire_speed = 800
    torped_speed = 8

    def __init__(self, path: str, x:int, y:int,
                 HP_max=100,
                 velocity=4.0,
                 fire_speed=800,
                 torpedo_speed=8
                 ) -> None:
        super().__init__(path, velocity, x, y)
        self.torpedo:List[Torpedo] = []
        self.last_fire_time = 0
        
        # skills var (can be improved)
        self.HP_max = HP_max
        self.HP = self.HP_max
        self.fire_speed = fire_speed
        self.torped_speed = torpedo_speed

    def reset(self):
        self.HP_max = Spaceship.HP_max
        self.HP = self.HP_max
        self.velocity = Spaceship.velocity
        self.fire_speed = Spaceship.fire_speed
        self.torped_speed = Spaceship.torpedo_speed

    def fire(self):
        if time.get_ticks() - self.last_fire_time >= self.fire_speed:
            self.torpedo.append(Torpedo("assets/torpedo.png",
                                        self.torped_speed,
                                        self.rect.center[0]-TORPEDO_SIZE/2,self.rect.y)
                                        )
            self.last_fire_time = time.get_ticks()

    # définission des méthodes d'amélioration de compétences


class Torpedo(Sprite.Sprite):
    # Basic stats
    damage = 100
    piercing = 1

    def __init__(self, path: str, velocity:float, x:int, y:int) -> None:
        super().__init__(path, velocity, x, y)
        self.damage = Torpedo.damage
        self.piercing = Torpedo.piercing
    
    def move(self):
        self.move_up()
    
    # définission des méthodes d'amélioration de compétences