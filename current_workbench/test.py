import pygame

from modules.Label import Label
from modules.colors import RGB
from time import sleep

pygame.init()

# Create a window 500x500
screen = pygame.display.set_mode((500, 500))

while True:
    
    # fill the window of orange color
    screen.fill(RGB("orange"))

    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            pygame.quit()
            exit()

        # if user press Esc so exit the program
        if evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
    
    # Create a Label
    label = Label(screen,
                    txt="Hello, World! \nIt's me Mario! It's me Mario!\nIt's me Mario!", 
                    topleft=(100, 100), 
                    border_size=1,
                    bg=RGB("blue"),
                    fg=RGB("black"),
                    padding=(5,5,5,5))

    # add the label to the screen
    label.draw()

    surface = pygame.Surface((100,100))
    surface.fill(RGB("red"))
    rect = surface.get_rect()

    screen.blit(surface,rect)

    # update the screen
    pygame.display.flip()
    sleep(1/10)
