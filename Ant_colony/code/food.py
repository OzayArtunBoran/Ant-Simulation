import pygame
import random
import numpy as np


class Food(pygame.sprite.Sprite):
    def __init__(self, x, y, quantity=10):
        super().__init__()
        self.x = x
        self.y = y
        self.quantity = quantity  # Başlangıç yiyecek miktarı
        self.image = pygame.transform.scale(pygame.image.load(
            "../images/corn.png").convert_alpha(), (32 // 4, 32 // 4))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.angle = random.uniform(0, 2 * np.pi)
        self.taken = False

    def take_food(self, amount=1):
        """
        Karınca tarafından yiyecek alınması.
        """
        if self.quantity > 0:
            self.quantity -= amount  # Miktarı azalt
        if self.quantity <= 0:
            self.kill()  # Yiyecek bitince nesneyi kaldır

    def draw(self, screen):
        """
        Yiyeceği ekranda çizer ve miktarına göre boyutunu günceller.
        """
        size = max(8, int(self.quantity * 1.5))  # Minimum boyut 8 piksel
        self.image = pygame.transform.scale(pygame.image.load(
            "../images/corn.png").convert_alpha(), (size, size))
        self.rotate_image = pygame.transform.rotate(
            self.image, np.degrees(self.angle))
        screen.blit(self.rotate_image, self.rect)

    def is_near_ant(self, ant):
        """
        Karınca yiyeceğe yakın mı? Mesafeyi kontrol eder.
        """
        distance = ((self.rect.centerx - ant.x)**2 +
                    (self.rect.centery - ant.y)**2)**0.5
        return distance < 10  # 10 pikselden yakınsa True döner

