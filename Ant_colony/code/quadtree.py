import pygame
from settings import *


class Point:
    def __init__(self, x, y, userdata=0):
        self.x = x
        self.y = y
        self.userdata = userdata


class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def contains(self, point):
        return (self.x <= point.x < self.x + self.w and
                self.y <= point.y < self.y + self.h)

    def intersect(self, other):
        return not (other.x - other.w > self.x + self.w or
                    other.x + other.w < self.x - self.w or
                    other.y - other.h > self.y + self.h or
                    other.y + other.h < self.y - self.h)


class Circle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def contains(self, point):
        point_distance_x = point.x - self.x
        point_distance_y = point.y - self.y
        return self.w**2 >= point_distance_x**2 + point_distance_y**2

    def intersect(self, range):
        circle_distance_x = abs(range.x - (self.x + self.w / 2))
        circle_distance_y = abs(range.y - (self.y + self.h / 2))
        if circle_distance_x > self.w / 2 + range.w:
            return False
        if circle_distance_y > self.h / 2 + range.h:
            return False
        if circle_distance_x <= self.w / 2:
            return True
        if circle_distance_y <= self.h / 2:
            return True
        corner_distance_sq = (circle_distance_x - self.w /
                            2)**2 + (circle_distance_y - self.h / 2)**2
        return corner_distance_sq <= range.w**2


class Quadtree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.northeast = None
        self.northwest = None
        self.southeast = None
        self.southwest = None
        self.divided = False

    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w
        h = self.boundary.h
        
        ne = Rectangle(x + w / 2, y, w / 2, h / 2)
        self.northeast = Quadtree(ne, self.capacity)
        
        nw = Rectangle(x, y, w / 2, h / 2)
        self.northwest = Quadtree(nw, self.capacity)
        
        se = Rectangle(x + w / 2, y + h / 2, w / 2, h / 2)
        self.southeast = Quadtree(se, self.capacity)
        
        sw = Rectangle(x, y + h / 2, w / 2, h / 2)
        self.southwest = Quadtree(sw, self.capacity)
        
        self.divided = True

    def insert(self, point):
        if not self.boundary.contains(point):
            return False
        
        if len(self.points) < self.capacity:
            self.points.append(point)
            return True
        else:
            if not self.divided:
                self.subdivide()
            
            if self.northeast.insert(point):
                return True
            elif self.northwest.insert(point):
                return True
            elif self.southeast.insert(point):
                return True
            elif self.southwest.insert(point):
                return True
        
        return False

    def query(self, range, found=None, pheromone_type=None):
        if found is None:
            found = []
        
        if not self.boundary.intersect(range):
            return found
        else:
            for p in self.points:
                if range.contains(p):
                    if pheromone_type is None or (hasattr(p.userdata, 'type') and p.userdata.type == pheromone_type):
                        found.append(p)
        
        if self.divided:
            self.northeast.query(range, found, pheromone_type)
            self.northwest.query(range, found, pheromone_type)
            self.southeast.query(range, found, pheromone_type)
            self.southwest.query(range, found, pheromone_type)
        
        return found

    def delete_point(self, point):
        if not self.boundary.contains(point):
            return
        
        if point in self.points:
            self.points.remove(point)
            return
        
        if self.divided:
            self.northeast.delete_point(point)
            self.northwest.delete_point(point)
            self.southeast.delete_point(point)
            self.southwest.delete_point(point)

# Yeni Quadtree'ler Oluşturma

class Simulation:
    def __init__(self):
        # Karıncalar için Quadtree
        ant_boundary = Rectangle(0, 0, WIDTH, HEIGHT)
        self.ant_qtree = Quadtree(ant_boundary, capacity=4)
        
        # Feromonlar için Quadtree
        pheromone_boundary = Rectangle(0, 0, WIDTH, HEIGHT)
        self.pheromone_qtree = Quadtree(pheromone_boundary, capacity=4)

    def add_ant(self, ant):
        point = Point(ant.x, ant.y, ant)
        self.ant_qtree.insert(point)

    def add_pheromone(self, pheromone):
        point = Point(pheromone.x, pheromone.y, pheromone)
        self.pheromone_qtree.insert(point)

    def update(self):
        # Karıncaların güncellenmesi
        for ant in self.ant_qtree.points:
            if hasattr(ant.userdata, 'type') and ant.userdata.type == 'worker':
                # Eğer işçi karınca tehdit algılarsa, yuvaya döner ve tehdit feromonu salgılar
                if ant.userdata.detect_threat():
                    ant.userdata.leave_pheromone('threat')
                    ant.userdata.return_to_nest()
                else:
                    # Normalde yiyecek feromonu takip eder
                    ant.userdata.leave_pheromone('food')
                    ant.userdata.search_for_food()
            elif hasattr(ant.userdata, 'type') and ant.userdata.type == 'soldier':
                # Asker karıncalar sadece tehdit feromonlarını takip eder
                ant.userdata.follow_pheromone('threat')
            
            ant.userdata.update()
            self.ant_qtree.insert(Point(ant.userdata.x, ant.userdata.y, ant.userdata))
        
        # Feromonların güncellenmesi
        for pheromone in self.pheromone_qtree.points:
            pheromone.userdata.update()
            self.pheromone_qtree.insert(Point(pheromone.userdata.x, pheromone.userdata.y, pheromone.userdata))

    def find_pheromones_by_type(self, pheromone_type, search_area):
        return self.pheromone_qtree.query(search_area, pheromone_type=pheromone_type)
