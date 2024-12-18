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
        ne = Rectangle(x + w/2, y, w/2, h/2)
        self.northeast = Quadtree(ne, self.capacity)
        nw = Rectangle(x, y, w/2, h/2)
        self.northwest = Quadtree(nw, self.capacity)
        se = Rectangle(x + w/2, y + h/2, w/2, h/2)
        self.southeast = Quadtree(se, self.capacity)
        sw = Rectangle(x, y + h/2, w/2, h/2)
        self.southwest = Quadtree(sw, self.capacity)
        self.divided = True

    def insert(self, point):
        if not self.boundary.contains(point):
            return
        if not self.divided:
            if len(self.points) < self.capacity:
                if len(self.points) <= 2000:
                    self.points.append(point)
            else:
                self.subdivide()
                if len(self.points) <= 2000:
                    self.points.append(point)
                for pnt in self.points:
                    self.northeast.insert(pnt)
                    self.northwest.insert(pnt)
                    self.southeast.insert(pnt)
                    self.southwest.insert(pnt)
                self.points.clear()
        else:
            self.northeast.insert(point)
            self.northwest.insert(point)
            self.southeast.insert(point)
            self.southwest.insert(point)

    def delete_point(self, point):
        if not self.boundary.contains(point):
            return
        elif not self.divided:
            for i in range(len(self.points)):
                if self.points[i].x == point.x and self.points[i].y == point.y:
                    self.points.pop(i)
                    return
        else:
            self.northeast.delete_point(point)
            self.northwest.delete_point(point)
            self.southeast.delete_point(point)
            self.southwest.delete_point(point)

    def query(self, range, found=None):
        if found is None:
            found = []
        if not self.boundary.intersect(range):
            return
        else:
            for p in self.points:
                if range.contains(p):
                    found.append(p)
        if self.divided:
            self.northeast.query(range, found)
            self.northwest.query(range, found)
            self.southeast.query(range, found)
            self.southwest.query(range, found)
            return found

    def draw(self, screen):
        pygame.draw.rect(screen, (56, 56, 221),
                         (self.boundary.x,
                         self.boundary.y, self.boundary.w,
                          self.boundary.h), 1)

        if self.divided:
            self.northeast.draw(screen)
            self.northwest.draw(screen)
            self.southeast.draw(screen)
            self.southwest.draw(screen)

    def draw_points(self, screen):
        if self.divided:
            self.northeast.draw_points(screen)
            self.northwest.draw_points(screen)
            self.southeast.draw_points(screen)
            self.southwest.draw_points(screen)
        else:
            for point in self.points:
                pygame.draw.circle(screen, '#5495e8',
                                   (point.x, point.y), 1)
