import pygame
from pygame.draw import *
import numpy as np

clock = pygame.time.Clock()
pygame.init()
FPS = 30

# цвета
purple = (140, 78, 148)
yellow = (255, 255, 0)
red = (155, 30, 30)
orange = (250, 150, 0)
light_yellow = (240, 187, 74)
pink = (255, 199, 199)
dark_purple = (28, 0, 33)

# размеры
SCALE = 0.3
SCREEN_WIDTH = round(2500 * SCALE)
SCREEN_HEIGHT = round(1667 * SCALE)
SUN_RADIUS = round(140 * SCALE)

# цвета частей
SUN_COLOR = yellow
BACKGROUND_1_COLOR = light_yellow
BACKGROUND_2_COLOR = pink
BACKGROUND_3_COLOR = light_yellow
BACKGROUND_4_COLOR = purple
MOUNTAINS_1_COLOR = orange
MOUNTAINS_2_COLOR = red
MOUNTAINS_3_COLOR = dark_purple
BIRD_COLOR = dark_purple

# расположение частей
SUN_POSITION = round(1175 * SCALE), round(360 * SCALE)
BACKGROUND_2_POSITION = round(360 * SCALE)
BACKGROUND_3_POSITION = round(715 * SCALE)
BACKGROUND_4_POSITION = round(1100 * SCALE)
MOUNTAINS_1_COORDINATES = [[0, 776], [0, 678], [514, 330], [608, 357], [652, 419], [960, 629],
                           [1127, 603], [1211, 648], [1335, 529], [
                               1440, 554], [1501, 500], [1819, 264],
                           [1869, 305], [1982, 411], [2072, 392], [2242, 476], [2325, 430], [2500, 517], [0, 776]]
MOUNTAINS_2_COORDINATES = [[0, 832], [64, 864], [221, 669], [433, 1066], [545, 879], [721, 974], [800, 752],
                           [1021, 800],
                           [1200, 932], [1433, 884], [1712, 680], [2041, 883], [
                               2152, 750], [2254, 821], [2304, 740],
                           [2402, 750], [2500, 590], [2500, 1074], [0, 1129]]
MOUNTAINS_3_COORDINATES = [[0, 857], [293, 936], [536, 1231], [796, 1574], [1171, 1638], [1584, 1412], [1695, 1460],
                           [1865, 1511], [2094, 1388], [2371, 1074], [2500, 1000], [2500, 1667], [0, 1667]]
BIRDS_COORDINATES_AND_SIZES = [[993, 778, 1], [959, 604, 1], [1186, 624, 1], [1184, 708, 1], [1567, 1133, 1.2],
                               [1706, 1255, 1], [1987, 1209, 0.9], [1949, 1337, 1.4]]

# масштабирование координат гор
for point in MOUNTAINS_1_COORDINATES:
    point[0] = round(point[0] * SCALE)
    point[1] = round(point[1] * SCALE)
for point in MOUNTAINS_2_COORDINATES:
    point[0] = round(point[0] * SCALE)
    point[1] = round(point[1] * SCALE)
for point in MOUNTAINS_3_COORDINATES:
    point[0] = round(point[0] * SCALE)
    point[1] = round(point[1] * SCALE)


# функция, рисующая птицу
def draw_bird(screen, color, x, y, size, time):
    BIRD_COORDINATES = [[x, y],
                        [x + round(81 * size), (y - round(46 * size)) * (1 + np.sin(time) / 50)],
                        [x + round(29 * size), (y - round(39 * size)) * (1 + np.sin(time) / 50)],
                        [x + round(7 * size), y - round(23 * size)],
                        [x - round(48 * size), (y - round(44 * size)) * (1 + np.sin(time) / 50)],
                        [x - round(72 * size), (y - round(41 * size)) * (1 + np.sin(time) / 50)],
                        [x, y]]
    for point in BIRD_COORDINATES:
        point[0] = round(point[0] * SCALE)
        point[1] = round(point[1] * SCALE)
    polygon(screen, color, BIRD_COORDINATES)


# экран
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.update()
finished = False
time = 0

alpha = np.random.random(len(BIRDS_COORDINATES_AND_SIZES))

while not finished:
    time += 0.1
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
    # задний фон
    rect(screen, BACKGROUND_1_COLOR, (0, 0, SCREEN_WIDTH, BACKGROUND_2_POSITION - 0))
    rect(screen, BACKGROUND_2_COLOR, (0, BACKGROUND_2_POSITION,
                                      SCREEN_WIDTH, BACKGROUND_3_POSITION - BACKGROUND_2_POSITION))
    rect(screen, BACKGROUND_3_COLOR, (0, BACKGROUND_3_POSITION,
                                      SCREEN_WIDTH, BACKGROUND_4_POSITION - BACKGROUND_3_POSITION))
    rect(screen, BACKGROUND_4_COLOR, (0, BACKGROUND_4_POSITION,
                                      SCREEN_WIDTH, SCREEN_HEIGHT - BACKGROUND_2_POSITION))

    # горы
    polygon(screen, MOUNTAINS_1_COLOR, MOUNTAINS_1_COORDINATES)
    polygon(screen, MOUNTAINS_2_COLOR, MOUNTAINS_2_COORDINATES)
    polygon(screen, MOUNTAINS_3_COLOR, MOUNTAINS_3_COORDINATES)

    # Солнце
    circle(screen, SUN_COLOR, SUN_POSITION, SUN_RADIUS)

    # птицы
    i = 0
    for bird in BIRDS_COORDINATES_AND_SIZES:
        new_x = bird[0] * 1
        new_y = bird[1] * (1 + np.cos(alpha[i] * time) / 20)
        new_size = bird[2] * (1 + time ** 0.5 / 10)
        draw_bird(screen, BIRD_COLOR, new_x, new_y, new_size, time)

        i += 1

    pygame.display.update()

pygame.quit()
