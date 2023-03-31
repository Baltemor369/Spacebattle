import pygame


class Skills:
    def __init__(self,
                 hp:int,
                 att_speed:int,
                 att_velocity:int,
                 torpedo_dmg:int,
                 piercing:int
                 ) -> None:
        
        self.HP_max = hp
        self.att_speed = att_speed
        self.att_velocity = att_velocity
        self.torpedo_damage = torpedo_dmg
        self.torpedo_piercing = piercing