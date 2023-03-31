
from typing import List,Union
from pygame import time,Rect
import modules.Sprite as Sprite
import modules.Skills as Skills

TORPEDO_SIZE = 16


class Spaceship(Sprite.Sprite, Skills.Skills):
    # Basic stats
    HP_bonus = 50
    velocity_bonus = 1
    att_speed_bonus = 100
    att_velocity_bonus = 1
    torpedo_damage_bonus = 50
    torpedo_piercing_bonus = 1
                                                # path, pos, HP_max, velocity, att_speed, att_velocity, torpedo_damage, torpedo_piercing, display]
    def __init__(self, args:Union[object, list]) -> None:

        if type(args) == list:
            Sprite.Sprite.__init__(self, args[0], args[3], args[1], display=args[8])
            Skills.Skills.__init__(self, args[2], args[4], args[5], args[6], args[7])

            self.HP = self.HP_max
            self.torpedo:List[Torpedo] = []
            self.last_fire_time = 0
            self.last_collision = 0
        else:
            self.__dict__.update(args.__dict__)
        

    def fire(self):
        if time.get_ticks() - self.last_fire_time >= self.att_speed:
            self.torpedo.append(Torpedo("assets/torpedo.png",
                                        self.att_velocity,
                                        (self.rect.x + (self.rect.w - TORPEDO_SIZE) / 2, self.rect.y),
                                        self.torpedo_damage,
                                        self.torpedo_piercing,
                                        True
                                        )
                                )
            self.last_fire_time = time.get_ticks()
    
    def take_damage(self, damage:int) -> None:
        self.HP -= damage
        if self.HP < 0:
            self.HP = 0

    def HP_upgrade(self):
        self.HP_max += Spaceship.HP_bonus
    
    def velocity_upgrade(self):
        self.velocity += Spaceship.velocity_bonus
    
    def att_speed_upgrade(self):
        self.att_speed += Spaceship.att_speed_bonus
    
    def att_velo_upgrade(self):
        self.att_velocity += Spaceship.att_velocity_bonus
    
    def damage_upgrade(self):
        self.torpedo_damage += Spaceship.torpedo_damage_bonus
    
    def piercing_upgrade(self):
        self.torpedo_piercing += Spaceship.torpedo_piercing_bonus


class Torpedo(Sprite.Sprite):

    def __init__(self,
                 path:str,
                 velocity:float,
                 pos:Union[tuple[float,float],Rect],
                 damage:int,
                 piercing:int,
                 disp:bool
                 ) -> None:
        
        super().__init__(path, velocity, pos, disp)

        self.damage = damage
        self.piercing = piercing
    
    def move(self):
        self.move_up()
    
    def collision(self):
        self.piercing -= 1