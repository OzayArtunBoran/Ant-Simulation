# main.py - Ant Colony Simülasyonu

import pygame
import random
from settings import *
from ant import Worker, Soldier, Queen
from pheromone import PheromoneManager
from food import Food
from quadtree import Quadtree, Rectangle, Point

class Setup:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Ant Colony')
        icon = pygame.image.load('../images/ant_ico.png')
        pygame.display.set_icon(icon)
        surf = pygame.transform.scale(pygame.image.load(
            "../images/corn.png").convert_alpha(), (32 // 2, 32 // 2))
        cursor = pygame.cursors.Cursor((0, 0), surf)
        pygame.mouse.set_cursor(cursor)
        self.clock = pygame.time.Clock()
        self.delta_time = self.clock.tick(FPS)

    def draw_nest(self):
        nest = pygame.transform.scale(pygame.image.load(
            "../images/nest.png").convert_alpha(), (32 * 3, 32 * 3))
        nest_rect = nest.get_rect(center=(NEST_X, NEST_Y))
        self.screen.blit(nest, nest_rect)
        return nest_rect

    def create_objects(self):
        # Karınca grupları oluşturuluyor
        self.worker_ants = pygame.sprite.Group(
            [Worker(self.delta_time) for _ in range(INITIAL_WORKERS)])
        self.soldier_ants = pygame.sprite.Group(
            [Soldier(self.delta_time) for _ in range(INITIAL_SOLDIERS)])
        self.foods = pygame.sprite.Group(
            [Food(random.randint(1000, WIDTH - 100),
                  random.randint(600, HEIGHT - 100)) for _ in range(FOOD)])
        self.pheromone_manager = PheromoneManager()
        self.queen = Queen()

    def pheromone_quadtree(self):
        pheromone_boundary = Rectangle(0, 0, WIDTH, HEIGHT)
        self.pheromone_qtree = Quadtree(pheromone_boundary, 4)

    def ant_quadtree(self):
        ant_boundary = Rectangle(0, 0, WIDTH, HEIGHT)
        self.ant_qtree = Quadtree(ant_boundary, 4)

    def user_event(self):
        self.add_pheromone_event = pygame.USEREVENT
        pygame.time.set_timer(self.add_pheromone_event, 100)

    def update_ants(self, ant_group, nest):
        for ant in ant_group:
            if isinstance(ant, Worker):
                if ant.detect_threat(self.pheromone_qtree):
                    ant.return_to_nest(self.screen, nest, self.pheromone_qtree)
                else:
                    ant.search_for_food(self.screen, self.foods, self.pheromone_qtree)
                    self.pheromone_manager.leave_pheromone(ant, 'food', PHEROMONE_LIFESPAN, self.pheromone_qtree)
            elif isinstance(ant, Soldier):
                ant.follow_threat_pheromone(self.pheromone_qtree)
                self.pheromone_manager.leave_pheromone(ant, 'threat', PHEROMONE_LIFESPAN, self.pheromone_qtree)
            ant.update(self.screen, nest, self.foods, self.ant_qtree, self.pheromone_qtree, self.queen)
            ant.draw(self.screen)

    def main(self):
        self.create_objects()
        self.pheromone_quadtree()
        self.ant_quadtree()
        self.user_event()

        while True:
            self.screen.fill(SAND)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    food = Food(*mouse_pos)
                    self.foods.add(food)
                elif event.type == self.add_pheromone_event:
                    # Kraliçe karınca üretim süreci
                    new_ant = self.queen.produce()
                    if new_ant:
                        if isinstance(new_ant, Worker):
                            self.worker_ants.add(new_ant)
                        elif isinstance(new_ant, Soldier):
                            self.soldier_ants.add(new_ant)

            # Feromonları güncelle
            self.pheromone_manager.update_pheromones(self.pheromone_qtree)
            self.pheromone_manager.draw_pheromones(self.screen)

            # Yuvayı çiz
            nest = self.draw_nest()

            # Yemleri çiz
            for food in self.foods:
                food.draw(self.screen)

            # Quadtree'leri güncelle
            self.ant_quadtree()

            # Karınca gruplarını güncelle
            self.update_ants(self.worker_ants, nest)
            self.update_ants(self.soldier_ants, nest)

            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    setup_instance = Setup()
    setup_instance.main()
