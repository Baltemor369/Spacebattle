import pygame
from pygame.locals import *
from typing import Union
from modules.Padding import Padding

pygame.init()

BLACK = (0,0,0)

class Label:
    """ This class is used to more easily create labels with pygame. """
    font = pygame.font.Font(None, 21)

    def __init__(self,
                 root_surface:pygame.Surface,
                 txt:Union[str,list[str]],
                 topleft:Union[tuple, pygame.Rect, None]=None,
                 topright:Union[tuple, pygame.Rect, None]=None,
                 bottomleft:Union[tuple, pygame.Rect, None]=None,
                 bottomright:Union[tuple, pygame.Rect, None]=None,
                 size:Union[tuple[int,int],None]=None,
                 bg:Union[tuple[int,int,int],None]=None,
                 fg:Union[tuple[int,int,int],None]=None,
                 border_color:Union[tuple[int,int,int],None]=BLACK,
                 border_size:int=1,
                 padding:Union[tuple[float,float,float,float],Padding]=Padding(),
                 display:bool = True,
                 text_align:str="center"
                 ) -> None:
        """
        Initialize a new object of Label class.

        args:
            root_surface (pygame.Surface): The surface that the label will be drawn on.
            txt (str | list): The text that will be displayed, str or a list of strings.
            topleft (tuple, pygame.Rect, None): The top left position of the label, a tuple(x,y) or pygame.Rect object.
            topright (tuple, pygame.Rect, None): The top right position of the label, a tuple(x,y) or pygame.Rect object.
            bottomleft (tuple, pygame.Rect, None): The bottom left position of the label, a tuple(x,y) or pygame.Rect object.
            bottomright (tuple, pygame.Rect, None): The bottom right position of the label, a tuple(x,y) or pygame.Rect object.
            size (tuple, None): The size of the label, a tuple(width,height) or None.
            bg (tuple, None): The background color of the label, a tuple(r,g,b) or None.
            fg (tuple, None): The foreground color of the label, a tuple(r,g,b) or None.
            border_color (tuple, None): The color of the border of the label, a tuple(r,g,b) or None.
            border_size (int): The size of the border of the label.
            padding (tuple, Padding): The padding of the label, a tuple(top,bottom,right,left) or Padding object.
            display (bool): Whether the label will be displayed or not.
            text_align (str): The alignment of the text, either "left", "center" or "right".        
        """
        
        self.root_s = root_surface
        self.size = size
        if type(txt) == str:
            self._txt = txt.split("\n")
        else:
            self._txt = txt
        self._align = text_align
        
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
            self._padding = Padding(padding[0],padding[1],padding[2],padding[3])
        else:
            self._padding = padding

        if self.size is None or type(self.size) is not tuple:
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
        if topleft is not None:
            if type(topleft) == tuple:
                self.rect.topleft = topleft
            elif type(topleft) == pygame.Rect:
                self.rect.topleft = topleft.topleft
            else:
                self.rect.topleft = (0,0)
        
        elif topright is not None:
            if type(topright) == tuple:
                self.rect.topright = topright
            elif type(topright) == pygame.Rect:
                self.rect.topright = topright.topright
            else:
                self.rect.topright = (0,0)
        
        elif bottomleft is not None:
            if type(bottomleft) == tuple:
                self.rect.bottomleft = bottomleft
            elif type(bottomleft) == pygame.Rect:
                self.rect.bottomleft = bottomleft.bottomleft
            else:
                self.rect.bottomleft = (0,0)
        
        elif bottomright is not None:
            if type(bottomright) == tuple:
                self.rect.bottomright = bottomright
            elif type(bottomright) == pygame.Rect:
                self.rect.bottomright = bottomright.bottomright
            else:
                self.rect.bottomright = (0,0)
        

        for i,line in enumerate(self._txt):
            # Create a surface for the text
            text_surface = self.font.render(line, True, self._fg)
            
            # Create a rect for the text
            size = (self.size[0] - self._padding.left - self._padding.right,
                    self.size[1] - self._padding.top - self._padding.bottom)
            if self._align == "center":
                x = self._padding.left + (size[0] - text_surface.get_width())/2
                y = self._padding.top + i * text_surface.get_height()
            elif self._align == "left":
                x = self._padding.left
                y = self._padding.top + i * text_surface.get_height()
            elif self._align == "right":
                x = self.size[0] - self._padding.right - text_surface.get_width()
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
        """
        Resize the label.

        args:
            w (int): the new_width of the label.
            h (int): the new_height of the label.
        """
        self.__init__(root_surface=self.root_s,
                      txt=self._txt,
                      topleft=self.rect.topleft,
                      topright=self.rect.topright,
                      bottomleft=self.rect.bottomleft,
                      bottomright=self.rect.bottomright,
                      size=(w,h),
                      bg=self._bg,
                      fg=self._fg,
                      border_color=self._border_color,
                      border_size=self._border_size,
                      padding=self._padding,
                      display=self._display,
                      text_align=self._align)
