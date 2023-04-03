
from typing import List,Union
from pygame import time,Rect
from modules.Sprite import Sprite
from modules.Skills import Skills

TORPEDO_SIZE = 16


class Spaceship(Sprite, Skills):
    """ This class is used to create a special Sprite with skills and abilities."""
    
    # Basic stats
    HP_bonus = 50
    velocity_bonus = 1
    att_speed_bonus = 100
    att_velocity_bonus = 1
    damage_bonus = 50
    piercing_bonus = 0.5
                                                # path, pos, HP_max, velocity, att_speed, att_velocity, damage, piercing, display]
    def __init__(self, __o:object=None,**kwargs) -> None:
        """
        Initializes a new object of the Padding class.

        args:
            args (Spaceship): a other instance of class Spaceship to initialize this one.
            kwargs (dict): dictionnary with initialize parameters.
        
        dict args:
            path (str): access path to the picture for the Sprite.
            coord (tuple | Rect): position of the Sprite on the screen, tuple(x,y) or pygame.Rect.
            hp (int): maximum HP of the Sprite.
            velocity (int): velocity of the Sprite.
            att_speed (int): attack speed of the Sprite.
            att_velocity (int): attack's velocity of the Sprite.
            damage (int): damage of the Sprite.
            piercing (int): number of elements that can be passed through before exploding.
            invicible_time (int): time (ms) during which the player is invincible
            display (bool): if the player is displayed or not.
        """
        keys=["path", "coord", "hp", "velocity", "att_speed", "att_velocity", "damage", "piercing", "display", "invicible_time"]

        if len(kwargs) == 10 and __o is None:
            if all(key in kwargs.keys() for key in keys):
                Sprite.__init__(self, path=kwargs["path"],
                                velocity=kwargs["velocity"],
                                coord=kwargs["coord"],
                                invicible_time=kwargs["invicible_time"],
                                display=kwargs["display"]
                                )
                Skills.__init__(self, hp=kwargs["hp"],
                                att_speed=kwargs["att_speed"],
                                att_velocity=kwargs["att_velocity"],
                                damage=kwargs["damage"],
                                piercing=kwargs["piercing"])

                self.HP = self.HP_max
                self.torpedo:List[Torpedo] = []
                self.last_fire_time = 0

        elif __o is not None and len(kwargs)==0:
            self.__dict__.update(__o.__dict__)
        else:
            return -1 # code error

    def fire(self, direction:str):
        """
        Fires a torpedo in the given direction.
        
        args:
            direction (str): direction of the torpedo (up-down-left-right).

        """
        if time.get_ticks() - self.last_fire_time >= self.att_speed:
            self.torpedo.append(Torpedo("assets/torpedo.png",
                                        self.att_velocity,
                                        (self.rect.x + (self.rect.w - TORPEDO_SIZE) / 2, self.rect.y),
                                        self.damage,
                                        self.piercing,
                                        self.invicible_time,
                                        True,
                                        direction
                                        )
                                )
            self.last_fire_time = time.get_ticks()
    
    def take_damage(self, damage:int) -> None:
        """
        Takes damage and decreases HP.

        args:
            damage (int): amount of damage to take.
        """
        if self.collable:
            self.HP -= damage
            self.last_collision = time.get_ticks()
            self.collable = (time.get_ticks() - self.last_collision >= self.invicible_time)

        if self.HP < 0:
            self.HP = 0

    def HP_upgrade(self):
        """
        Increases HP by HP_bonus.
        """
        self.HP_max += Spaceship.HP_bonus
    
    def velocity_upgrade(self):
        """
        Increases velocity by velocity_bonus.
        """
        self.velocity += Spaceship.velocity_bonus
    
    def att_speed_upgrade(self):
        """
        Increases velocity by att_speed_bonus.
        """
        self.att_speed -= Spaceship.att_speed_bonus
    
    def att_velo_upgrade(self):
        """
        Increases velocity by att_velocity_bonus.
        """
        self.att_velocity += Spaceship.att_velocity_bonus
    
    def damage_upgrade(self):
        """
        Increases velocity by damage_bonus.
        """
        self.damage += Spaceship.damage_bonus
    
    def piercing_upgrade(self):
        """
        Increases velocity by piercing_bonus.
        """
        self.piercing += Spaceship.piercing_bonus

    def manage_torpedo(self):
        """
        Manages torpedoes movement.
        """
        for elt in self.torpedo:
            elt.move()
class Torpedo(Sprite):
    """ This class is used for creating Sprite able to deal damage to other Sprite"""
    def __init__(self,
                 path:str,
                 velocity:float,
                 pos:Union[tuple[float,float],Rect],
                 damage:int,
                 piercing:int,
                 invicible_time:int,
                 disp:bool,
                 dir:str
                 ) -> None:
        """
        Initilize a new object of Torpedo class.

        args:
            path (str): acces path to the image of the torpedo.
            velocity (int): the velocity of the torpedo.
            pos (tuple | Rect): position  of the torpedo type of tuple(x,y) or a Rect object.
            damage (int): damage amount of the torpedo.
            piercing (int): number of elements that can be passed through before exploding.
            invicible_time (int): time (ms) during which the player is invincible 
            disp (boll): if the torpedo is displayed or not.
            dir (str): direction of the torpedo (up-down-left-right).
        """
        super().__init__(path, velocity, pos, invicible_time, disp)

        self.dir = dir.lower()
        self.damage = damage
        self.piercing = piercing
    
    def move(self):
        """
        Move the torpedo according to self.dir.
        """
        match self.dir:
            case "up":
                self.move_up()
            case "down":
                self.move_down()
            case "left":
                self.move_left()
            case "right":
                self.move_right()
    
    def change_fir(self, dir:str):
        """
        Change the direction of the torpedo.
        """
        if dir.lower() in ["up","down","left","right"]:
            self.dir = dir.lower()
    
    def collision(self):
        """
        decrease self.piercing cause of one collision.
        """
        self.piercing -= 1
