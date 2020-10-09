import pygame
import pygame.draw
from random import randint
import numpy as np
import os.path

FPS = 30
W_WIDTH, W_HEIGHT = 800, 600
dt = 0.01

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


class Square:
    def __init__(self, screen, player_points):
        self.points = randint(50, 100)
        self.points += int((player_points / 2) ** 0.5)

        self.x = randint(int(W_WIDTH * 0.1), int(W_WIDTH * 0.9))
        self.y = randint(int(W_HEIGHT * 0.1), int(W_HEIGHT * 0.9))

        self.a = int(2 * (W_WIDTH + W_HEIGHT) / self.points)

        self.vx = randint(0, 100 + int(self.points**0.5 * 10))
        self.vy = randint(0, 100 + int(self.points**0.5 * 10))

        self.color = COLORS[randint(0, 5)]
        self.image = pygame.draw.rect(screen, self.color, (int(self.x - self.a / 2),
                                                           int(self.y - self.a / 2),
                                                           self.a, self.a)
                                      )

    def hit(self, event):
        hit = False
        if abs(self.x - event.pos[0]) <= self.a / 2 and  \
                abs(self.y - event.pos[1]) <= self.a / 2:
            hit = True
        return hit

    def move(self, screen):
        if self.x + self.a / 2 + self.vx * dt >= W_WIDTH or\
                self.x - self.a / 2 + self.vx * dt <= 0:
            self.vx *= -1
        if self.y + self.a / 2 + self.vy * dt >= W_HEIGHT or\
                self.y - self.a / 2 + self.vy * dt <= 0:
            self.vy *= -1

        self.x += self.vx * dt
        self.y += self.vy * dt

        self.vx += randint(-(50 + int(self.points)), 50 + int(self.points))
        self.vy += randint(-(50 + int(self.points)), 50 + int(self.points))

        self.vx = np.sign(self.vx) * min(abs(self.vx), self.points * 10)
        self.vy = np.sign(self.vy) * min(abs(self.vy), self.points * 10)

        self.image = pygame.draw.rect(screen, self.color, (int(self.x - self.a / 2),
                                                           int(self.y - self.a / 2),
                                                           self.a, self.a)
                                      )


class Ball:
    def __init__(self, screen, player_points):
        self.points = randint(20, 50)
        self.points += int((player_points / 5))

        self.x = randint(int(W_WIDTH * 0.1), int(W_WIDTH * 0.9))
        self.y = randint(int(W_HEIGHT * 0.1), int(W_HEIGHT * 0.9))

        self.r = int((W_WIDTH + W_HEIGHT) / self.points)

        self.vx = randint(int(self.points * 20), 100 + int(self.points * 20))
        self.vy = randint(int(self.points * 20), 100 + int(self.points * 20))

        self.color = COLORS[randint(0, 5)]
        self.image = pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)

    def hit(self, event):
        hit = False
        if ((self.x - event.pos[0]) ** 2 + (self.y - event.pos[1]) ** 2) ** 0.5 <= self.r:
            hit = True
        return hit

    def move(self, screen):
        self.x += self.vx * dt
        self.y += self.vy * dt

        if self.x + self.r >= W_WIDTH or self.x - self.r <= 0:
            self.vx *= -1

        if self.y + self.r >= W_HEIGHT or self.y - self.r <= 0:
            self.vy *= -1

        self.image = pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.r)


def write_to_file(points):
    """Writes points, scored in this game, to file data.txt.

    :param points: points scored in one game.
    """
    output = open("data.txt", 'a')
    print(points, file=output)
    output.close()


def read_from_file():
    """Calculates highest score.

    :return: maximum of all the points written in data.txt.
    """
    inp = open("data.txt", 'r')

    max_points = 0
    for line in inp:
        if int(line) > max_points:
            max_points = int(line)

    return max_points


def display_score(screen, max_points, points):
    """ Displays highest score and current score.

    :param screen: screen, on which the game is being drawn.
    :param max_points: highest point ever scored.
    :param points: points scored in this game.
    """
    font = pygame.font.SysFont('Comic Sans MS', 30)

    text_max_points = font.render("Highest score: " + str(max_points),
                                  False, (200, 200, 200))
    text_points = font.render("Score: " + str(points),
                              False, (200, 200, 200))
    screen.blit(text_max_points, (0, 0))
    screen.blit(text_points, (0, 50))


def main():
    pygame.init()
    screen = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
    pygame.display.update()
    clock = pygame.time.Clock()
    finished = False

    points = 0
    balls = [Ball(screen, points) for i in range(1)]
    squares = [Square(screen, points) for i in range(2)]

    if not os.path.isfile('C:/Users/Dmitr/khromov/lab_4/data.txt'):
        output = open("data.txt", 'w')
        output.close()
    max_points = read_from_file()

    while not finished:
        clock.tick(FPS)

        display_score(screen, max_points, points)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                i = 0
                hit = False
                for ball in balls:
                    if ball.hit(event):
                        balls[i] = Ball(screen, points)
                        points += ball.points
                        hit = True
                    i += 1
                i = 0
                for square in squares:
                    if square.hit(event):
                        squares[i] = Square(screen, points)
                        points += square.points
                        hit = True
                    i += 1
                if not hit:
                    points = max(0, points - 100)
        for ball in balls:
            ball.move(screen)
        for square in squares:
            square.move(screen)
        pygame.display.update()
        screen.fill(BLACK)

    write_to_file(points)

    pygame.quit()


if __name__ == "__main__":
    main()
