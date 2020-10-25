import pygame as pg
import numpy as np
from random import randint

FPS = 30
SCREEN_SIZE = [800, 600]

BLACK = (0, 0, 0)
RED = (255, 0, 0)


class Ball:
    """
    Creates balls, manages their movement, collisions, rendering.
    """
    def __init__(self, coord, vel, rad=15, color=None):
        """
        Creates a ball with given initial conditions.
        """
        if color is None:
            color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.color = color
        self.coord = coord
        self.vel = vel
        self.rad = rad
        self.is_alive = True

    def draw(self, screen):
        """
        Draws the ball on the screen.
        """
        pg.draw.circle(screen, self.color, self.coord, self.rad)

    def move(self, t_step=1., g=1.):
        """
        Moves the ball. Velocity of the ball is also changed due to gravity.
        """
        self.vel[1] += int(g * t_step)
        for i in range(2):
            self.coord[i] += int(self.vel[i] * t_step)
        self.check_walls()
        if self.vel[0]**2 + self.vel[1]**2 < 2**2 and\
                self.coord[1] > SCREEN_SIZE[1] - 2*self.rad:
            self.is_alive = False

    def check_walls(self):
        """
        Checks if the ball has collided with walls and calls flip_vel method to change its velocity if it did.
        """
        n = [[1, 0], [0, 1]]
        for i in range(2):
            if self.coord[i] < self.rad:
                self.coord[i] = self.rad
                self.flip_vel(n[i])
            elif self.coord[i] > SCREEN_SIZE[i] - self.rad:
                self.coord[i] = SCREEN_SIZE[i] - self.rad
                self.flip_vel(n[i])

    def flip_vel(self, axis, coef_perp=0.8, coef_par=0.9):
        """
        Changes the velocity of the ball as if it collided inelastically with a wall with normal vector "axis".
        """
        vel = np.array(self.vel)
        n = np.array(axis)
        n = n / np.linalg.norm(n)
        vel_perp = vel.dot(n) * n
        vel_par = vel - vel_perp
        ans = -vel_perp * coef_perp + vel_par * coef_par
        self.vel = ans.astype(np.int).tolist()


class Target:
    """
    Creates targets, manages their collisions with balls, rendering.
    """
    def __init__(self, coord, rad=30, color=None):
        """
        Creates a target with given initial conditions.
        """
        if color is None:
            color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.color = color
        self.coord = coord
        self.rad = rad
        self.is_alive = True

    def draw(self, screen):
        """
        Draws the target on the screen.
        """
        pg.draw.circle(screen, self.color, self.coord, self.rad)

    def check_collision(self, ball):
        """
        Checks if the ball collided with the target.
        """
        distance = (sum((ball.coord[i] - self.coord[i])**2 for i in range(2)))**0.5
        return distance <= self.rad + ball.rad


class Gun:
    """
    Creates a gun, manages its movement, shooting, aiming and rendering.
    """
    def __init__(self, coords=None, min_pow=10, max_pow=40):
        """
        Creates a gun with given initial conditions.
        """
        if coords is None:
            coords = [30, SCREEN_SIZE[1] // 2]
        self.coords = coords
        self.angle = 0
        self.min_pow = min_pow
        self.max_pow = max_pow
        self.power = min_pow
        self.active = False

    def draw(self, screen):
        """
        Draws a gun on the screen.
        """
        end_pos = [int(self.coords[0] + self.power * np.cos(self.angle)),
                   int(self.coords[1] + self.power * np.sin(self.angle))]
        pg.draw.line(screen, RED, self.coords, end_pos, 5)

    def shoot(self):
        """
        Creates a ball. Velocity of the ball depends on where the gun is pointing and how much power it has.
        """
        vel = [int(self.power * np.cos(self.angle)),
               int(self.power * np.sin(self.angle))]
        self.active = False
        self.power = self.min_pow
        return Ball(list(self.coords), vel)

    def gain_power(self):
        """
        Increases the gun's power.
        """
        if self.active and self.power < self.max_pow:
            self.power += 1

    def set_angle(self, mouse_pos):
        """
        Changes the angle of the gun.
        """
        self.angle = np.arctan2(mouse_pos[1] - self.coords[1],
                                mouse_pos[0] - self.coords[0])


class ScoreTable:
    pass


class Manager:
    """
    Manages the process of the game.
    """
    def __init__(self):
        """
        Creates a game: guns, balls, targets and a score table.
        """
        self.gun = Gun()
        self.table = ScoreTable()
        self.balls = []
        self.targets = []

    def process(self, events, screen):
        """
        Manages the game. If all the targets have been hit, creates new ones.
        """
        done = self.handle_events(events)

        if len(self.targets) == 0 and len(self.balls) == 0:
            self.targets = [Target([randint(100, SCREEN_SIZE[0] - 30), randint(30, SCREEN_SIZE[1] - 30)])
                            for i in range(3)]

        self.check_collisions()
        self.check_alive()
        self.move()
        self.draw(screen)

        return done

    def draw(self, screen):
        """
        Draws all the objects, which have to drawn on the screen.
        """
        screen.fill(BLACK)
        self.gun.draw(screen)
        for ball in self.balls:
            ball.draw(screen)
        for target in self.targets:
            target.draw(screen)

    def move(self):
        """
        Moves all the objects, which have to be moved.
        """
        for ball in self.balls:
            ball.move()
        self.gun.gain_power()

    def check_alive(self):
        """
        Checks if the balls are still moving and if the targets have not been hit yet.
        """
        dead_balls = []
        for i, ball in enumerate(self.balls):
            if not ball.is_alive:
                dead_balls.append(i)
        for i in reversed(dead_balls):
            self.balls.pop(i)
        dead_targets = []
        for i, target in enumerate(self.targets):
            if not target.is_alive:
                dead_targets.append(i)
        for i in reversed(dead_targets):
            self.targets.pop(i)

    def check_collisions(self):
        """
        Checks if the balls have hit some targets.
        """
        for target in self.targets:
            for ball in self.balls:
                if target.check_collision(ball):
                    target.is_alive = False

    def handle_events(self, events):
        """
        Handles the events.
        """
        done = False
        for event in events:
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.gun.coords[1] -= 5
                elif event.key == pg.K_DOWN:
                    self.gun.coords[1] += 5
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.gun.active = True
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    self.balls.append(self.gun.shoot())

        if pg.mouse.get_focused():
            mouse_pos = pg.mouse.get_pos()
            self.gun.set_angle(mouse_pos)

        return done


def main():
    """
    Creates a screen, starts a game by calling a manager.
    """
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
