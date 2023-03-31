import pygame
from pygame.locals import *
from typing import Union
import modules.Padding as Padding

pygame.init()

BLACK = (0,0,0)
LIGHT_GREY = (int(255/2),int(255/2),int(255/2))
WHITE = (255,255,255)


class Label:
    font = pygame.font.Font(None, 21)

    def __init__(self,
                 root_surface:pygame.Surface,
                 txt:str,
                 coord:Union[tuple, pygame.Rect],
                 size:Union[tuple[int,int],None]=None,
                 bg:Union[tuple[int,int,int],None]=None,
                 fg:Union[tuple[int,int,int],None]=None,
                 border_color:Union[tuple[int,int,int],None]=BLACK,
                 border_size:int=1,
                 padding:Union[tuple[float,float,float,float],Padding.Padding]=Padding.Padding(),
                 display:bool = True
                 ) -> None:
        
        self.root_s = root_surface
        self.size = size
        self._txt = txt.split("\n")
        
        if bg is None:
            self._bg = pygame.SRCALPHA
        else:
            self._bg = bg
        
        if fg is None:
            self._fg = self._bg
        else:
            self._fg = fg
        
        if border_color is None:
            self._border_color = self._bg
        else:
            self._border_color = border_color
        
        self._border_size = border_size
        self._display = display
        
        if type(padding) == tuple:
            self._padding = Padding.Padding(padding[0],padding[1],padding[2],padding[3])
        else:
            self._padding = padding

        if self.size is None or type(self.size) is not tuple[int,int]:
            self.size = (0,0)
            for line in self._txt:
                buffer = Label.font.render(line, True, self._fg)
                if self.font.size(line)[0] > self.size[0]:
                    self.size = self.font.size(line)[0], self.size[1]
                self.size = self.size[0], self.size[1] + buffer.get_height()
            
            self.size = (self.size[0] + self._padding.left + self._padding.right,
                         self.size[1] + self._padding.top + self._padding.bottom)

        # Create the Surface
        if bg is None:
            self.surface = pygame.Surface((self.size[0], self.size[1]), self._bg)
        else:
            self.surface = pygame.Surface((self.size[0], self.size[1]))
            self.surface.fill(self._bg)

        # Create the Rect
        self.rect = self.surface.get_rect()
        if type(coord) == tuple:
            self.rect.topleft = coord[0], coord[1]
        elif type(coord) == pygame.Rect:
            self.rect.topleft = coord.topleft
        else:
            self.rect.topleft = (0,0)

        for i,line in enumerate(self._txt):
            # Create a surface for the text
            text_surface = self.font.render(line, True, self._fg)
            
            # Create a rect for the text
            x = self._padding.left + (self.size[0]-self._padding.left-self._padding.right)/2 - text_surface.get_width()/2
            y = self._padding.top + i * text_surface.get_height()
            text_rect = text_surface.get_rect(topleft=(x,y))
            
            # Add the text to the surface with a padding
            self.surface.blit(text_surface, text_rect)

        # draw border
        if self._border_size > 0:
            pygame.draw.rect(self.surface, self._border_color, self.surface.get_rect(), border_size)

    # Create a method to display the label on the root surface
    def draw(self):
        """
        Draw the label on the root surface.
        """
        if self._display:
            self.root_s.blit(self.surface, self.rect)

    def resize(self, w:int , h:int):
        self.__init__(self.root_s,
                      self._txt,
                      self.rect,
                      (w,h),
                      self._bg,
                      self._fg,
                      self._border_color,
                      self._border_size,
                      self._padding,
                      self._display)
