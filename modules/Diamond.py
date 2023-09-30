import pygame
from pygame.locals import *
import random
from constants.constants import SIZE, SRC_DIAMOND

class Diamond:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load(SRC_DIAMOND).convert()
        self.x = 850
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 20)*SIZE
        self.y = random.randint(1, 12)*SIZE