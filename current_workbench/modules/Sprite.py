import pygame

# une class qui va gérer tout ce qui est mouvement et localisation des objets
class Sprite(pygame.sprite.Sprite):
    def __init__(self, path:str, velocity:float, x:int, y:int) -> None:
        super().__init__()
        self.velocity = velocity
        self.img = pygame.image.load(path)
        
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move_up(self):
        self.rect.y -= self.velocity
    def move_down(self):
        self.rect.y += self.velocity
    def move_left(self):
        self.rect.x -= self.velocity
    def move_right(self):
        self.rect.x += self.velocity
