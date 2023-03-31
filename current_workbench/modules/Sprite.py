from pygame import Rect, image, sprite
from typing import Union

class Sprite(sprite.Sprite):
    
    def __init__(self, path:str, velocity:float, coord:Union[tuple[float,float], Rect], display:bool=True) -> None:
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
        self.rect.y -= self.velocity
    def move_down(self) -> None:
        self.rect.y += self.velocity
    def move_left(self) -> None:
        self.rect.x -= self.velocity
    def move_right(self) -> None:
        self.rect.x += self.velocity
    
    def set_pos(self, pos:Union[tuple[float,float],Rect]) -> None:
        if type(pos) == tuple:
            self.rect.x = pos[0]
            self.rect.y = pos[1]
        else:
            self.rect.x = pos.x
            self.rect.y = pos.y

    def get_pos(self) -> tuple[float, float]:
        return (self.rect.x, self.rect.y)