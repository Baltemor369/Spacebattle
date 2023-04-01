from pygame import Rect, image, sprite
from typing import Union

class Sprite(sprite.Sprite):
    """ This class is used for elements that can move on a surface. """
    def __init__(self, path:str, velocity:float, coord:Union[tuple[float,float], Rect], display:bool=True) -> None:
        """
        Initialize a new object of Sprite class.

        args:
            path (str): access path to the image of the sprite
            velocity (int): the speed of the sprite
            coord (tuple | Rect): the position of the sprite on the surface, tuple(x,y) or a pygame.Rect.
            display (bool): if the sprite should be displayed
        """
        super().__init__()
        
        self.img = image.load(path)
        self.display = display
        self.velocity = velocity
        self.rect = self.img.get_rect()
        self.collable = True

        if type(coord) == tuple:
            self.rect.x = coord[0]
            self.rect.y = coord[1]
            
        elif type(coord) == type(Rect):
            self.rect.x = coord.x
            self.rect.y = coord.y

    def move_up(self) -> None:
        """ Move the sprite up. """
        self.rect.y -= self.velocity
    def move_down(self) -> None:
        """ Move the sprite down. """
        self.rect.y += self.velocity
    def move_left(self) -> None:
        """ Move the sprite left. """
        self.rect.x -= self.velocity
    def move_right(self) -> None:
        """ Move the sprite right. """
        self.rect.x += self.velocity
    
    def set_pos(self, pos:Union[tuple[float,float],Rect]) -> None:
        """ 
        Set the position of the sprite. 

        args:
            pos (tuple | Rect): the position of the sprite on the surface, tuple(x,y) or a pygame.Rect Object.
        """
        if type(pos) == tuple:
            self.rect.x = pos[0]
            self.rect.y = pos[1]
        else:
            self.rect.x = pos.x
            self.rect.y = pos.y

    def get_pos(self) -> tuple[float, float]:
        """
        Get the position of the sprite.

        returns:
            tuple: the position of the sprite on the surface, tuple(x,y)
        """
        return (self.rect.x, self.rect.y)