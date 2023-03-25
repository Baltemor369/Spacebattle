import pygame


class Skills:
    def __init__(self,
                 hp:int,
                 speed:float,
                 att_speed:int,
                 att_velocity:int,
                 torpedo_dmg:int,
                 piercing:int
                 ) -> None:
        
        self.HP_max = hp
        self.speed = speed
        self.att_speed = att_speed
        self.att_velocity = att_velocity
        self.torpedo_damage = torpedo_dmg
        self.torpedo_piercing = piercing

"""
button -    Img? NAME    button +
"""