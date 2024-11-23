# pheromone.py - Pheromone Sınıfı ve Yeni Pheromone Yönetimi

import pygame
from settings import *
from quadtree import *

class Pheromone(pygame.sprite.Sprite):
    def __init__(self, x, y, pheromone_type, lifespan):
        super().__init__()
        self.x = x
        self.y = y
        self.type = pheromone_type  # Feromon türü (yiyecek, tehdit, yol bulma)
        self.lifespan = lifespan  # Feromonun ömrü
        self.base_size = (5, 5)
        self.image = pygame.Surface(self.base_size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # Feromon türüne göre renklendirme
        if self.type == 'food':
            self.color = (0, 255, 0, 128)  # Yeşil - Yiyecek feromonu
        elif self.type == 'threat':
            self.color = (255, 0, 0, 128)  # Kırmızı - Tehdit feromonu
        elif self.type == 'trail':
            self.color = (0, 0, 255, 128)  # Mavi - Yol bulma feromonu
        else:
            self.color = (255, 255, 255, 128)  # Varsayılan beyaz

        pygame.draw.circle(self.image, self.color, (self.base_size[0] // 2, self.base_size[1] // 2), self.base_size[0] // 2)

    def update(self, pheromone_qtree):
        # Feromonun ömrünü azalt
        self.lifespan -= 1
        if self.lifespan <= 0:
            pheromone_qtree.delete_point(Point(self.x, self.y, self))
            self.kill()  # Feromonun ömrü bittiğinde kaldır

    def draw(self, screen):
        # Feromonu ekranda çiz
        screen.blit(self.image, self.rect)

# Yeni feromon ekleme ve yönetme fonksiyonları
class PheromoneManager:
    def __init__(self):
        self.pheromones = pygame.sprite.Group()

    def add_pheromone(self, x, y, pheromone_type, lifespan, pheromone_qtree):
        pheromone = Pheromone(x, y, pheromone_type, lifespan)
        self.pheromones.add(pheromone)
        pheromone_qtree.insert(Point(x, y, pheromone))

    def leave_pheromone(self, ant, pheromone_type, lifespan, pheromone_qtree):
        # Karıncanın bulunduğu konumda feromon bırakma işlemi
        pheromone = Pheromone(ant.x, ant.y, pheromone_type, lifespan)
        self.pheromones.add(pheromone)
        pheromone_qtree.insert(Point(ant.x, ant.y, pheromone))

    def update_pheromones(self, pheromone_qtree):
        # Tüm feromonları güncelle
        for pheromone in self.pheromones:
            pheromone.update(pheromone_qtree)

    def draw_pheromones(self, screen):
        # Tüm feromonları ekrana çiz
        for pheromone in self.pheromones:
            pheromone.draw(screen)
