import pygame
from typing import Union

class Sprite(pygame.sprite.Sprite):
    
    def __init__(self, path:str, velocity:float, coord:Union[tuple[int,int], pygame.Rect], display:bool=True) -> None:
        super().__init__()
        
        self.img = pygame.image.load(path)
        self.display = display
        self.velocity = velocity
        self.rect = self.img.get_rect()

        if type(coord) == tuple:
            self.rect.x = coord[0]
            self.rect.y = coord[1]
            
        elif type(coord) == type(pygame.Rect):
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
    
    def set_pos(self, x:int, y:int) -> None:
        self.rect.x = x
        self.rect.y = y

    def get_pos(self) -> tuple[int, int]:
        return (self.rect.x, self.rect.y)