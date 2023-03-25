
from typing import List,Union
from pygame import time,Rect
import modules.Sprite as Sprite
import modules.Skills as Skills

TORPEDO_SIZE = 16


class Spaceship(Sprite.Sprite, Skills.Skills):
    # Basic stats
    # HP_bonus = 100
    # velocity_bonus = 3
    # att_speed_bonus = 800
    # att_velocity_bonus = 8
    # torpedo_dmg_bonus = 100
    # torpedo_piercing_bonus = 1

    def __init__(self, path: str, 
                 pos:Union[tuple[int,int], Rect],
                 HP_max:int,
                 velocity:float,
                 att_speed:int,
                 att_velocity:int,
                 torpedo_dmg:int,
                 torpedo_piercing:int,
                 display:bool=True
                 ) -> None:
        
        Sprite.Sprite.__init__(self, path, velocity, pos, display=display)
        Skills.Skills.__init__(self, HP_max,
                               velocity,
                               att_speed,
                               att_velocity,
                               torpedo_dmg,
                               torpedo_piercing
                               )

        self.HP = self.HP_max
        self.torpedo:List[Torpedo] = []
        self.last_fire_time = 0

    def fire(self):
        
        if time.get_ticks() - self.last_fire_time >= self.att_speed:
            self.torpedo.append(Torpedo("assets/torpedo.png",
                                        self.att_velocity,
                                        self.rect.center[0] - TORPEDO_SIZE / 2,
                                        self.rect.y,
                                        self.torpedo_damage,
                                        self.torpedo_piercing,
                                        True
                                        )
                                )
            self.last_fire_time = time.get_ticks()
    
    def take_damage(self, dmg:int) -> None:
        self.HP -= dmg
        if self.HP < 0:
            self.HP = 0


class Torpedo(Sprite.Sprite):

    def __init__(self,
                 path:str,
                 velocity:float,
                 x:int, y:int,
                 damage:int,
                 piercing:int,
                 disp:bool
                 ) -> None:
        
        super().__init__(path, velocity, (x, y), disp)

        self.damage = damage
        self.piercing = piercing
    
    def move(self):
        self.move_up()
    
    def collision(self):
        self.piercing -= 1