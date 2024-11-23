# ant.py - Ant Sınıfı ve Yeni Karınca Sınıfları

import pygame
import random
import numpy as np
from settings import *
from quadtree import *
from pheromone import PheromoneManager

class Ant(pygame.sprite.Sprite):
    def __init__(self, delta_time=1, health=100):
        super().__init__()
        self.delta_time = delta_time
        self.speed = 0.3 * delta_time
        self.index = 0
        self.size = (IMAGE_W / 3, IMAGE_H / 3)
        self.move = [pygame.transform.scale(pygame.image.load(
            f'../images/ant{i}.png').convert_alpha(), self.size) for i in range(1, 9)]
        self.x = NEST_X
        self.y = NEST_Y
        self.image = self.move[self.index]
        self.rect = self.image.get_rect()
        self.angle = random.uniform(0, 2 * np.pi)
        self.choose = 0
        self.encountered_pheromones = set()
        self.encountered_foods = set()
        self.dragged_food = None
        self.health = health  # Karınca sağlığı
        self.lifespan = ANT_LIFESPAN  # Karıncanın yaşam süresi
        self.alive = True  # Karıncanın canlılık durumu

    def kill(self):
        self.alive = False
        self.health = 0

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()

    def update(self, screen, nest, foods, ant_quad_tree, pheromone_qtree, queen):
        # Yaşam süresi ve sağlık kontrolü
        self.lifespan -= 0.1
        if self.lifespan <= 0 or self.health <= 0:
            self.kill()
            return

        self.speedx = self.speed * np.cos(self.angle)
        self.speedy = -self.speed * np.sin(self.angle)

        self.x += self.speedx
        self.y += self.speedy

        self.image = self.move[self.index // 2]
        if self.index < 15:
            self.index += 1
        else:
            self.index = 0

        self.collision(ant_quad_tree)

        self.wrap_around()

        self.image, self.rect = self.rotate_center()

        if self.choose == 0:
            self.search_for_food(screen, foods, pheromone_qtree)
        elif self.choose == 1:
            self.return_to_nest(screen, nest, pheromone_qtree)

        # Queen üretim süreci
        new_ant = queen.produce()
        if new_ant:
            if isinstance(new_ant, Worker):
                ant_quad_tree.insert(Point(new_ant.x, new_ant.y, new_ant))
            elif isinstance(new_ant, Soldier):
                ant_quad_tree.insert(Point(new_ant.x, new_ant.y, new_ant))

    def leave_pheromone(self, pheromone_manager, pheromone_type, lifespan, pheromone_qtree):
        pheromone_manager.leave_pheromone(self, pheromone_type, lifespan, pheromone_qtree)

    # Diğer metodlar ...
    def wrap_around(self):
        if self.x < 15:
            angel_d = self.angle_direction(-0.25, 0.25)
            self.angle += angel_d * 0.1
        elif self.x >= WIDTH-15:
            angel_d = self.angle_direction(0.75, 1.25)
            self.angle += angel_d * 0.1
        elif self.y < 15:
            angel_d = self.angle_direction(1.25, 1.75)
            self.angle += angel_d * 0.1
        elif self.y >= HEIGHT-15:
            angel_d = self.angle_direction(0.25, 0.75)
            self.angle += angel_d * 0.1

    def angle_direction(self, start, end):
        angle_dir = random.uniform(start * np.pi, end * np.pi)
        angle_direct = self.angle_different(angle_dir)
        return angle_direct

    def angle_different(self, direction):
        angle_diff = (direction - self.angle +
                      np.pi) % (2 * np.pi) - np.pi
        return angle_diff

    def draw_view(self, angle):  # , screen, color
        self.center_x, self.center_y = self.rect.center
        rect_center_x = self.center_x + 25 * np.cos(self.angle + angle)
        rect_center_y = self.center_y - 25 * np.sin(self.angle + angle)
        visible_range = Circle(rect_center_x, rect_center_y, 10, 10)
        # pygame.draw.circle(screen, color, (visible_range.x,
        #                                    visible_range.y), visible_range.w, 1)
        return visible_range
    

    def search_for_food(self, screen, foods, pheromone_qtree):
        dist_list = []
        for j in range(3):
            visible_range = self.draw_view(ANGLES[j])  # screen, COLORS[j],
            found = pheromone_qtree.query(visible_range)
            if found:
                untaken_foods = list(set(
                    food for food in foods if not food.taken))
                if untaken_foods:
                    random_food = random.choice(untaken_foods)
                    for f in found:
                        # pygame.draw.circle(screen, BLUE, (f.x, f.y), 3)
                        points = (f.x, f.y)
                        goal = [(random_food.x, random_food.y)]
                        dist_to = self.get_closest_point(points, goal)
                        dist_list.append((f.x, f.y, dist_to))
                        found.clear()
        if dist_list:
            angle_f = self.min_dist(dist_list)
            angel_d = self.angle_different(angle_f)
            self.angle += angel_d * 0.1
            dist_list.clear()
        self.take_food(foods)

    def take_food(self, foods):
        f_collisions = pygame.sprite.spritecollide(self, foods, False)
        if f_collisions:
            for food in f_collisions:
                if food not in self.encountered_foods and not food.taken:
                    self.dragged_food = food
                    self.encountered_foods.add(self.dragged_food)
                    self.angle += np.pi
                    food.taken = True
                    self.choose = 1
                    break

    def return_to_nest(self, screen, nest, pheromone_qtree):
        dist_list = []
        for j in range(3):
            visible_range = self.draw_view(ANGLES[j])  # screen, COLORS[j],
            found = pheromone_qtree.query(visible_range)
            if found:
                for f in found:
                    # pygame.draw.circle(screen, RED, (f.x, f.y), 3)
                    points = (f.x, f.y)
                    goal = (NEST_X, NEST_Y)
                    dist_to = self.get_closest_point(points, goal)
                    dist_list.append((f.x, f.y, dist_to))
                    found.clear()
        if dist_list:
            angle_f = self.min_dist(dist_list)
            angel_d = self.angle_different(angle_f)
            self.angle += angel_d * 0.1
            dist_list.clear()
        self.drop_food_in_nest(nest)

    def drop_food_in_nest(self, nest):
        if self.rect.colliderect(nest):
            if self.dragged_food is not None:
                self.dragged_food.kill()
                self.dragged_food = None
                self.angle += np.pi
            self.choose = 0

    def rotate_center(self):
        self.rotate_image = pygame.transform.rotate(
            self.image, np.degrees(self.angle))
        self.rotate_rect = self.rotate_image.get_rect(center=self.rect.center)
        return self.rotate_image, self.rotate_rect

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        # pygame.draw.rect(screen, (255, 0, 0), self.rect, 1)
        self.rect.center = (self.x, self.y)

    def ant_coord(self):
        self.food_center_x = self.x + DISTANCE * \
            np.cos(self.angle)
        self.food_center_y = self.y - DISTANCE * \
            np.sin(self.angle)
        return self.food_center_x, self.food_center_y

    def get_closest_point(self, points, goal):
        p1 = np.array(points)
        p2 = np.array(goal)
        dist_to = np.linalg.norm(p1 - p2)
        return dist_to

    def min_dist(self, dist):
        min_distance = min(dist, key=lambda x: x[2])
        min_p_x, min_p_y, _ = min_distance
        angle_calc = self.arctan_calc(min_p_x, min_p_y)
        angle_f = np.pi/2 - angle_calc
        return angle_f

    def arctan_calc(self, x, y):
        angle = np.arctan2(x - self.x, self.y - y)
        return angle

    def intersects(self, other):
        return self.rect.colliderect(other.rect)

    def update_angle(self):
        self.angle += random.uniform(-6 * np.pi / 180, 6 * np.pi / 180)

    def collision(self, ant_quad_tree):
        point_p = Point(self.x, self.y, self)
        ant_quad_tree.insert(point_p)
        range_area = Rectangle(
            self.rect.x, self.rect.y, self.rect.w, self.rect.h)
        ant_found = ant_quad_tree.query(range_area)
        if ant_found:
            for f in ant_found:
                other_ant = f.userdata
                if self != other_ant and\
                        self.intersects(other_ant):
                    self.update_angle()
                    other_ant.update_angle()

class Worker(Ant):
    def __init__(self, delta_time=1, health=100):
        super().__init__(delta_time, health)
        self.pheromone_manager = PheromoneManager()  # Feromon yöneticisi ekleniyor

    def search_for_food(self, screen, foods, pheromone_qtree):
        # İşçi karınca yiyecek arar ve yiyecek feromonu bırakır
        super().search_for_food(screen, foods, pheromone_qtree)
        self.leave_pheromone(self.pheromone_manager, 'food', PHEROMONE_LIFESPAN, pheromone_qtree)

    def detect_threat(self, pheromone_qtree):
        # Tehdit algılama - Tehdit feromonlarını kontrol eder
        search_area = Rectangle(self.x - RADIUS, self.y - RADIUS, RADIUS * 2, RADIUS * 2)
        threats = pheromone_qtree.query(search_area, pheromone_type='threat')
        return len(threats) > 0

    def return_to_nest(self, screen, nest, pheromone_qtree):
        # Yuvaya geri dönme ve tehdit feromonu bırakma
        self.leave_pheromone(self.pheromone_manager, 'threat', PHEROMONE_LIFESPAN, pheromone_qtree)
        self.choose = 1
        super().return_to_nest(screen, nest, pheromone_qtree)

class Soldier(Ant):
    def __init__(self, delta_time=1, health=100):
        super().__init__(delta_time, health)
        self.pheromone_manager = PheromoneManager()  # Feromon yöneticisi ekleniyor

    def follow_threat_pheromone(self, pheromone_qtree):
        # Asker karınca tehdit feromonunu takip eder
        search_area = Rectangle(self.x - RADIUS, self.y - RADIUS, RADIUS * 2, RADIUS * 2)
        threats = pheromone_qtree.query(search_area, pheromone_type='threat')
        if len(threats) > 0:
            closest_threat = min(threats, key=lambda t: np.hypot(t.x - self.x, t.y - self.y))
            self.angle = np.arctan2(self.y - closest_threat.y, closest_threat.x - self.x)
            self.choose = 0

    def leave_pheromone(self, pheromone_manager, pheromone_type, lifespan, pheromone_qtree):
        pheromone_manager.leave_pheromone(self, pheromone_type, lifespan, pheromone_qtree)

class Queen():
    def __init__(self):
        self.stress = 0  # Stres seviyesi negatifse asker, pozitifse işçi üretilir; 0 iken beklenir
        self.countWorkers = 0
        self.countSoldiers = 0
        self.totalAntCount = self.countWorkers + self.countSoldiers

    def produce(self):
        if self.stress < 0:
            # Asker üret
            new_soldier = Soldier()
            self.countSoldiers += 1
            self.totalAntCount = self.countWorkers + self.countSoldiers
            return new_soldier
        elif self.stress > 0:
            # İşçi üret
            new_worker = Worker()
            self.countWorkers += 1
            self.totalAntCount = self.countWorkers + self.countSoldiers
            return new_worker
        else:
            # Bekle
            return None
