import pygame
import random
import numpy as np


class Food(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(pygame.image.load(
                "../images/hamburger.png").convert_alpha(), (32, 32))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.angle = random.uniform(0, 2 * np.pi)
        self.taken = False

        self.type = type
        if self.type == 'food':
            self.image = pygame.transform.scale(pygame.image.load(
                "../images/hamburger.png").convert_alpha(), (32, 32))
        elif self.type == 'threat':
            self.image = pygame.transform.scale(pygame.image.load(
            "../images/threat.png").convert_alpha(), (64, 64))

    def draw(self, screen):
        self.rotate_image = pygame.transform.rotate(
            self.image, np.degrees(self.angle))
        screen.blit(self.rotate_image, self.rect)
