import pygame
from pygame.locals import *

pygame.init()

screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bouton avec bordure")

button_width = 100
button_height = 50
button_x = 50
button_y = 50

button_surface = pygame.Surface((button_width, button_height))
button_rect = button_surface.get_rect()
button_rect.x = button_x
button_rect.y = button_y

button_surface.fill((255, 255, 255))

button_border_width = 2
button_border_color = (0, 0, 0)
pygame.draw.rect(button_surface, button_border_color, button_surface.get_rect(), button_border_width)

font = pygame.font.Font(None, 30)
text = font.render("Cliquez ici", True, (0, 0, 0))
text_rect = text.get_rect(center=button_surface.get_rect().center)
button_surface.blit(text, text_rect)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        elif event.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if button_rect.collidepoint(mouse_pos):
                print("Bouton cliqué !")

    screen.blit(button_surface, button_rect)
    pygame.display.update()
