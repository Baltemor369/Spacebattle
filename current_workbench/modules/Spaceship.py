
from typing import List
from pygame import time
import modules.Sprite as Sprite

TORPEDO_SIZE = 16


# class pour les attribut(HP boost etc) particulier des objet (player ennemy boss)
class Spaceship(Sprite.Sprite):
    def __init__(self, path: str, velocity:int, HP:int, x:int, y:int) -> None:
        super().__init__(path, velocity, x, y)
        self.HP_max = HP
        self.HP = HP
        self.torpedo:List[Torpedo] = []
        self.last_fire_time = 0
    
    def fire(self):
        if self.last_fire_time == 0 or time.get_ticks() - self.last_fire_time >= 1000:
            self.torpedo.append(Torpedo("./img/torpedo.png", 6, 100, self.rect.x+((self.rect.w-TORPEDO_SIZE)/2), self.rect.y))
            self.last_fire_time = time.get_ticks()


# class pour elt à dégâts (missiles)
class Torpedo(Sprite.Sprite):
    def __init__(self, path: str, velocity:int, damage:int, x:int, y:int) -> None:
        super().__init__(path, velocity, x, y)
        self.damage = damage
    
    def move(self):
        self.move_up()
    
