import numpy as np
from game_statistics import GameStatistics

global_stats_object = GameStatistics()

#screen settings
WIDTH = 1880
HEIGHT = 1000
FPS = 60

#ant settings
ANTS = 0
WORKER_ANTS = 0
SOLDIER_ANTS = 0
QUEEN_ANTS = 0
ANT_LIFESPAN = 100


FOOD_COUNT = 0

# karınca istatistikleri

#food settings
food = 1000 #toplam yiyecek sayısı

#image of ant
IMAGE_W = 65
IMAGE_H = 50

#nest settings
NEST_X, NEST_Y = 900, 500

#pheromone settings
DISTANCE = 10
RADIUS = 12

lifespan = 500

#colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0, 16)
SAND = (151, 125, 94)
P_BLUE = (84, 149, 232)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)

COLORS = [RED, GREEN, BLUE]
ANGLES = [0, -0.25*np.pi, 0.25*np.pi]
