import pygame
from pygame.locals import *
from typing import List, Union
pygame.init()

BLACK = (0,0,0)
LIGHT_GREY = (200,200,200)


class ButtonRect:
    font = pygame.font.Font(None, 20)

    def __init__(self,
                 w:int,
                 h:int,
                 coord:Union[tuple, pygame.Rect],
                 txt:str,
                 bg:tuple=LIGHT_GREY,
                 fg:tuple=BLACK,
                 border_color:tuple=BLACK,
                 display:bool = True
                 ) -> None:
        
        self._txt = txt
        self._bg = bg
        self._fg = fg
        self._border_color = border_color

        # Create the Surface
        self.surface = pygame.Surface((w,h))
        
        # Create the Rect
        self.rect = self.surface.get_rect()
        if type(coord) == tuple:
            self.rect.x = coord[0]
            self.rect.y = coord[1]
        elif type(coord) == pygame.Rect:
            self.rect.x = coord.x
            self.rect.y = coord.y

        self.display = display

        # Fill the surface with a color
        self.surface.fill(bg)

        # draw border
        pygame.draw.rect(self.surface, border_color, self.surface.get_rect(), 2)

        # Add a text
        text = ButtonRect.font.render(txt, True, fg)
        text_rect = text.get_rect(center=self.surface.get_rect().center)

        # Add the text to the button Surface 
        self.surface.blit(text, text_rect)

    def resize(self, w:int , h:int):
        self.__init__(w, h,
                      self.rect,
                      self._txt,
                      self._bg,
                      self._fg,
                      self._border_color,
                      self.display)
