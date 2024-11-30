import pygame
import random
import numpy as np
from settings import *
import time


class GameStatistics:
    def __init__(self):
        self.total_ants = 80 # başlangıç karınca sayısı
        self.total_food = 250 
        self.collected_food = 0
        self.temp_collected_food = 0
        self.taken_food = 0
        self.produced_ant_count  = 0
        self.collected_food_per_second  = 0
        self.collected_food_per_ant  = 0
        
    def increase_total_food(self):
        self.total_food = self.total_food + 1

    def increase_collected_food(self):
        self.collected_food = self.collected_food + 1
        return self.collected_food
    def increase_temp_collected_food(self):
        self.temp_collected_food = self.temp_collected_food + 1
        
    def increase_taken_food(self):
        self.taken_food = self.taken_food + 1
        
    def decrease_taken_food(self):
        self.taken_food = self.taken_food - 1
        
    def increase_produced_ant_count(self):
        self.produced_ant_count += 1
        self.total_ants += 1

    def increase_collected_food_per_second(self,start_time):
        self.current_time = pygame.time.get_ticks()
        self.elapsed_time = (self.current_time - start_time) // 1000
        self.collected_food_per_second = self.temp_collected_food // self.elapsed_time

    def recalculate_collected_food_per_ant(self):
        self.collected_food_per_ant = self.temp_collected_food / self.total_ants

    def decrease_collected_food_per_second(self):
        self.collected_food_per_second -= 1

    def decrease_produced_ant_count(self):
        self.produced_ant_count -= 1

    def decrease_collected_food(self):
        self.collected_food -= 1

    def reset_statistics(self):
        self.collected_food = 0
        self.produced_ant_count = 0
        self.collected_food_per_second = 0
        self.collected_food_per_ant = 0

    def retun_statistics(self):
        list = {
            "total_ants": self.total_ants, 
            "total_food": self.total_food,
            "collected_food": self.collected_food,
            "produced_ant_count": self.produced_ant_count,
            "collected_food_per_second": self.collected_food_per_second,
            "collected_food_per_ant": self.collected_food_per_ant
        }


        return list
    
