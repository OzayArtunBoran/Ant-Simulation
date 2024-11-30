import pygame
from settings import *
from quadtree import *


class Pheromone(pygame.sprite.Sprite): #ana feromon sınıfı
    def __init__(self, x, y, lifespan, pheromone_qtree, type, priority):
        super().__init__()
        self.x = x
        self.y = y
        self.type = type
        self.priority = priority
        if type == 'trace':
            self.lifespan = lifespan / 4 
        elif type == 'food':
            self.lifespan = lifespan * 3
        elif type == 'threat':
            self.lifespan = lifespan * 2

        self.base_size = (2, 2)
        self.image = pygame.Surface(self.base_size, pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.point = Point(self.x, self.y)
        pheromone_qtree.insert(self.point)


    def update(self, pheromone_qtree):
        self.lifespan -= 1
        if self.lifespan <= 0:
            pheromone_qtree.delete_point(self.point)
            self.kill() 

    def draw(self, screen):
        #eğer type trace ise mavi renkli feromon çizdir
        if self.type == 'trace':
            pygame.draw.circle(
                self.image, (84, 149, 232, 255), (1, 1), 3)
        #eğer type food ise yeşil renkli feromon çizdir
        elif self.type == 'food':
            pygame.draw.circle(
                self.image, (0, 255, 0, 255), (1, 1), 3)
        elif self.type == 'threat':
            pygame.draw.circle(
                self.image, (0, 255, 0, 255), (5, 5), 5) # tek tek tüm parametereler sırasıyla red, green, blue, alpha sonra radius değeri en son da thickness değeri
            
        self.rect.center = (self.x, self.y)
        screen.blit(self.image, self.rect)
