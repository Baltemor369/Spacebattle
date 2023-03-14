import pygame
import sys

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class UIpygame():
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.running = True
        self.player_img = pygame.image.load("img/spaceship.png").convert()

        self.clock = pygame.time.Clock()
    
    def handle_event(self):
        pass

    def update(self):
        pass

    def display(self):
        pass

    def run(self):
        
        while self.running:
            
            self.handle_event()
            
            self.update()
            
            self.display()

            for evt in pygame.event.get():
                if evt.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[]
            self.screen.blit(self.player_img, (0, 0))

            pygame.display.flip()

            self.clock.tick(60)


if __name__ == "__main__":
    game = UIpygame()
    game.run()
