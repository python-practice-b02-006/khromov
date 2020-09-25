import pygame
from pygame.draw import *

BLACK = (5, 5, 5)
GRAY = (200, 200, 200)
YELLOW = (180, 255, 0)
RED = (200, 0, 0)

pygame.init()

FPS = 30
W_WIDTH, W_HEIGHT = 400, 500

screen = pygame.display.set_mode([W_WIDTH, W_HEIGHT])

pygame.display.set_caption("Angry smile")


clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

    screen.fill(GRAY)

    radius = int((W_HEIGHT + W_WIDTH) / 8)
    circle(screen, YELLOW, (int(W_WIDTH / 2), int(W_HEIGHT / 2)), radius)

    circle(screen, RED, (int(1.25 * W_WIDTH / 2), int(0.85 * W_HEIGHT / 2)), int(radius / 8))
    circle(screen, BLACK, (int(1.25 * W_WIDTH / 2), int(0.85 * W_HEIGHT / 2)), int(radius / 16))
    circle(screen, RED, (int(0.75 * W_WIDTH / 2), int(0.85 * W_HEIGHT / 2)), int(radius / 5.5))
    circle(screen, BLACK, (int(0.75 * W_WIDTH / 2), int(0.85 * W_HEIGHT / 2)), int(radius / 13))

    line(screen, BLACK,
         (int(1.12 * W_WIDTH / 2), int(0.82 * W_HEIGHT / 2)),
         (int(1.45 * W_WIDTH / 2), int(0.7 * W_HEIGHT / 2)), 10)
    line(screen, BLACK,
         (int(0.9 * W_WIDTH / 2), int(0.82 * W_HEIGHT / 2)),
         (int(0.55 * W_WIDTH / 2), int(0.65 * W_HEIGHT / 2)), 10)

    rect(screen, BLACK, (int(0.75 * W_WIDTH / 2), int(1.2 * W_HEIGHT / 2),
                         int(0.5 * W_WIDTH / 2), int(0.09 * W_HEIGHT / 2)))
    pygame.display.update()

pygame.quit()
