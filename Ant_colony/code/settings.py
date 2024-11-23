import numpy as np

WIDTH = 1200
HEIGHT = 800

INITIAL_WORKERS = 10  # İlk işçi karınca sayısı
INITIAL_SOLDIERS = 5  # İlk asker karınca sayısı

FOOD = 2000
FPS = 60
IMAGE_W = 65
IMAGE_H = 50
NEST_X, NEST_Y = 600, 400

DISTANCE = 10
RADIUS = 12

HIVE_RESOURCES = 100
ANT_LIFESPAN = 50000

PHEROMONE_LIFESPAN = 500

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0, 16)
SAND = (151, 125, 94)
P_BLUE = (84, 149, 232)

COLORS = [RED, GREEN, BLUE]
ANGLES = [0, -0.25*np.pi, 0.25*np.pi]
