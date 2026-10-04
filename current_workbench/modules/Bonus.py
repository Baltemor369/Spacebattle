import pygame
import random
from modules.const import BONUS_SIZE, BONUS_VELOCITY

# kind: (color, letter, name shown to the player)
BONUS_TYPES = {
    "heal":   ((60, 220, 90), "+", "Soin"),
    "triple": ((250, 200, 40), "3", "Tir triple"),
    "shield": ((80, 200, 255), "S", "Bouclier"),
}


class Bonus(pygame.sprite.Sprite):
    """ This class is used for bonus falling from destroyed ennemys, picked up by the player. """
    _images = {}

    def __init__(self, kind:str, center:tuple[float,float]) -> None:
        """
        Initialize a new object of Bonus class.

        args:
            kind (str): type of the bonus, a key of BONUS_TYPES.
            center (tuple): center position of the bonus on the game surface.
        """
        super().__init__()
        self.kind = kind
        self.img = Bonus.image(kind)
        self.rect = self.img.get_rect(center=center)

    @staticmethod
    def random_kind() -> str:
        """ Returns a random type of bonus. """
        return random.choice(list(BONUS_TYPES))

    @staticmethod
    def name(kind:str) -> str:
        """ Returns the name of a type of bonus. """
        return BONUS_TYPES[kind][2]

    @staticmethod
    def image(kind:str) -> pygame.Surface:
        """
        Returns the picture of a type of bonus: a colored circle with a letter.
        Pictures are drawn once and shared by all bonus of the same type.
        """
        if kind not in Bonus._images:
            color, letter, _ = BONUS_TYPES[kind]
            img = pygame.Surface((BONUS_SIZE, BONUS_SIZE), pygame.SRCALPHA)
            radius = BONUS_SIZE // 2
            pygame.draw.circle(img, color, (radius, radius), radius)
            pygame.draw.circle(img, (255, 255, 255), (radius, radius), radius, 2)
            font = pygame.font.Font(None, 22)
            txt = font.render(letter, True, (20, 20, 20))
            img.blit(txt, txt.get_rect(center=(radius, radius + 1)))
            Bonus._images[kind] = img
        return Bonus._images[kind]

    def move(self) -> None:
        """ Move the bonus down. """
        self.rect.y += BONUS_VELOCITY
