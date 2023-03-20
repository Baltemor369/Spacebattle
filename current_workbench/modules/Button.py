import pygame
from pygame.locals import *
pygame.init()

BLACK = (0,0,0)
LIGHT_GREY = (200,200,200)


class Button:
    font = pygame.font.Font(None, 20)

    def __init__(self, w:int, h:int, x:int, y:int, txt:str) -> None:
        # Create the Surface
        self.surface = pygame.Surface((w,h))
        
        # Create the Rect
        self.rect = self.surface.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Fill the surface with a color
        self.surface.fill(LIGHT_GREY)

        pygame.draw.rect(self.surface, BLACK, self.surface.get_rect(), 2)

        # Add a text
        text = Button.font.render(txt, True, BLACK)
        text_rect = text.get_rect(center=self.surface.get_rect().center)

        # Add the text to the button Surface 
        self.surface.blit(text, text_rect)