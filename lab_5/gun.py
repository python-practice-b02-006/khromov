import pygame as pg
import numpy as np
from random import randint

FPS = 30
SCREEN_SIZE = [800, 600]

BLACK = (0, 0, 0)
RED = (255, 0, 0)

TIME_STEP = 0.01
GRAVITY = 10


class Ball:
    def __init__(self, coord, vel, rad=15, color=None):
        if color == None:
            color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.color = color
        self.coord = coord
        self.vel = vel
        self.rad = rad

    def draw(self, screen):
        pg.draw.circle(screen, self.color, self.coord, self.rad)

    def move(self, t_step=1.):
        for i in range(2):
            self.coord[i] += int(self.vel[i] * t_step)
        self.check_walls()

    def check_walls(self):
        n = [[1, 0], [0, 1]]
        for i in range(2):
            if self.coord[i] < self.rad:
                self.coord[i] = self.rad
                self.flip_vel(n[i])
            elif self.coord[i] > SCREEN_SIZE[i] - self.rad:
                self.coord[i] = SCREEN_SIZE[i] - self.rad
                self.flip_vel(n[i])

    def flip_vel(self, axis, coef_perp=1., coef_par=1.):
        vel = np.array(self.vel)
        n = np.array(axis)
        n = n / np.linalg.norm(n)
        vel_perp = vel.dot(n) * n
        vel_par = vel - vel_perp
        ans = -vel_perp * coef_perp + vel_par * coef_par
        print(vel, ans)
        self.vel = ans.astype(np.int).tolist()


class Target:
    pass


class Gun:
    def __init__(self, coords=[30, SCREEN_SIZE[1] // 2]):
        self.coords = coords
        self.angle = 0

    def draw(self, screen):
        end_pos = [int(self.coords[0] + 20 * np.cos(self.angle)),
                   int(self.coords[1] + 20 * np.sin(self.angle))]
        pg.draw.line(screen, RED, self.coords, end_pos, 5)

    def strike(self):
        pass

    def set_angle(self, mouse_pos):
        self.angle = np.arctan2(mouse_pos[1] - self.coords[1],
                                mouse_pos[0] - self.coords[0])


class ScoreTable:
    pass


class Manager:
    def __init__(self):
        self.gun = Gun()
        self.table = ScoreTable()
        self.balls = []
        self.balls.append(Ball([100, 100], [10, 20]))

    def process(self, events, screen):
        done = self.handle_events(events)

        self.move()
        self.draw(screen)

        return done

    def draw(self, screen):
        screen.fill(BLACK)
        self.gun.draw(screen)
        for ball in self.balls:
            ball.draw(screen)

    def move(self):
        for ball in self.balls:
            ball.move()

    def handle_events(self, events):
        done = False
        for event in events:
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.gun.coords[1] -= 5
                elif event.key == pg.K_DOWN:
                    self.gun.coords[1] += 5

        if pg.mouse.get_focused():
            mouse_pos = pg.mouse.get_pos()
            self.gun.set_angle(mouse_pos)

        return done


def main():
    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE)
    clock = pg.time.Clock()

    done = False

    manager = Manager()
    while not done:
        clock.tick(FPS)

        done = manager.process(pg.event.get(), screen)
        pg.display.update()

    pg.quit()


if __name__ == "__main__":
    main()
