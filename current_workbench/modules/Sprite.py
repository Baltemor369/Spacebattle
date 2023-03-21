import pygame

class Sprite(pygame.sprite.Sprite):
    def __init__(self, path:str, velocity:float, x:int, y:int) -> None:
        super().__init__()
        self.img = pygame.image.load(path)
        self.display = True
        self.collable_allowed = True

        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Skills var 
        self.velocity = velocity

    def move_up(self):
        self.rect.y -= self.velocity
    def move_down(self):
        self.rect.y += self.velocity
    def move_left(self):
        self.rect.x -= self.velocity
    def move_right(self):
        self.rect.x += self.velocity
    
    def set_pos(self, x:int, y:int):
        self.rect.x = x
        self.rect.y = y
