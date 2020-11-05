import pygame as pg
import numpy as np
from random import randint

FPS = 60
SCREEN_SIZE = [800, 600]
TIME_STEP = 0.5

BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


class Ball:
    """
    Creates balls, manages their movement, collisions, rendering.
    """
    def __init__(self, coords, vel, rad=15, color=None):
        """
        Creates a ball with given initial conditions.
        """
        if color is None:
            color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.color = color
        self.coords = np.array(coords, dtype=int)
        self.vel = np.array(vel, dtype=float)
        self.rad = rad
        self.is_alive = True

    def draw(self, screen):
        """
        Draws the ball on the screen.
        """
        pg.draw.circle(screen, self.color, self.coords, self.rad)

    def move(self, t_step=TIME_STEP, g=1.):
        """
        Moves the ball. Velocity of the ball is also changed due to gravity.
        """
        self.vel[1] += g * t_step
        self.coords += (self.vel * t_step).astype(int)
        self.check_walls()
        if np.linalg.norm(self.vel) < 1 and\
                self.coords[1] > SCREEN_SIZE[1] - 2 * self.rad:
            self.is_alive = False

    def check_walls(self):
        """
        Checks if the ball has collided with walls and calls flip_vel method to change its velocity if it did.
        """
        n = [[1, 0], [0, 1]]
        for i in range(2):
            if self.coords[i] < self.rad:
                self.coords[i] = self.rad
                self.flip_vel(n[i])
            elif self.coords[i] > SCREEN_SIZE[i] - self.rad:
                self.coords[i] = SCREEN_SIZE[i] - self.rad
                self.flip_vel(n[i])

    def flip_vel(self, axis, coef_perp=0.8, coef_par=0.9):
        """
        Changes the velocity of the ball as if it collided inelastically with a wall with normal vector "axis".
        """
        axis = np.array(axis)
        axis = axis / np.linalg.norm(axis)
        vel_perp = self.vel.dot(axis) * axis
        vel_par = self.vel - vel_perp
        self.vel = -vel_perp * coef_perp + vel_par * coef_par


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
        distance = (sum((ball.coords[i] - self.coord[i]) ** 2 for i in range(2))) ** 0.5
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
            coords = np.array([30, SCREEN_SIZE[1] // 2], dtype=int)
        self.coords = np.array(coords)
        self.angle = 0
        self.min_pow = min_pow
        self.max_pow = max_pow
        self.power = min_pow
        self.active = False

    def draw(self, screen):
        """
        Draws a gun on the screen.
        """
        end_pos = np.array([self.coords[0] + self.power * np.cos(self.angle),
                            self.coords[1] + self.power * np.sin(self.angle)], dtype=int)
        parallel = end_pos - self.coords
        normal = np.array([-parallel[1], parallel[0]], dtype=int)
        normal = np.array(5 * normal / np.linalg.norm(normal), dtype=int)

        vertexes = [self.coords + normal, self.coords - normal,
                    self.coords - normal + parallel, self.coords + normal + parallel]

        pg.draw.polygon(screen, RED, vertexes)

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
    """
    Manages counting of points and showing them to th player.
    """
    def __init__(self, targets_hit=0, balls_used=0):
        self.targets_hit = targets_hit
        self.balls_used = balls_used
        self.score = max(0, self.targets_hit - self.balls_used)

    def draw(self, screen):
        self.score = max(0, self.targets_hit - self.balls_used)

        font = pg.font.SysFont('Comic Sans MS', 30)

        text_targets_hit = font.render("Targets hit: " + str(self.targets_hit),
                                       False, (200, 200, 200))
        text_balls_used = font.render("Balls used: " + str(self.balls_used),
                                      False, (200, 200, 200))
        text_score = font.render("Score " + str(self.score),
                                 False, (200, 200, 200))
        screen.blit(text_targets_hit, (0, 0))
        screen.blit(text_balls_used, (0, 50))
        screen.blit(text_score, (0, 100))


class Wall:
    def __init__(self, length, width, angle=0, coords=None, color=None):
        """Creates a wall.

        :param length: length of the wall.
        :param width: width of the wall.
        :param angle: angle between the normal and x axis.
        :param coords: coordinates of the center of the wall.
        :param color: color of the wall.
        """
        if coords is None:
            coords = [SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2]
        self.angle = angle
        self.length = length
        self.width = width
        self.coords = np.array(coords, dtype=int)

        self.normal = np.array([np.cos(angle), -np.sin(angle)])
        self.parallel = np.array([np.sin(angle), np.cos(angle)])
        self.vertexes = np.array([self.coords + self.width * self.normal / 2 + self.length * self.parallel / 2,
                                  self.coords - self.width * self.normal / 2 + self.length * self.parallel / 2,
                                  self.coords - self.width * self.normal / 2 - self.length * self.parallel / 2,
                                  self.coords + self.width * self.normal / 2 - self.length * self.parallel / 2],
                                 dtype=int)

        if color is None:
            self.color = YELLOW

    def draw(self, screen):
        """
        Draws the wall on the screen.
        """
        pg.draw.polygon(screen, self.color, self.vertexes)

    def collision(self, ball):
        """
        Implements an elastic collision with the ball.
        """
        ball_coords = np.array([np.dot(ball.coords, self.normal),
                                np.dot(ball.coords, self.parallel)])
        wall_coords = np.array([np.dot(self.coords, self.normal),
                                np.dot(self.coords, self.parallel)])

        if abs(ball_coords[0] - wall_coords[0]) <= self.width / 2:
            if ball_coords[1] - ball.rad <= wall_coords[1] + self.length / 2 <= ball_coords[1]:
                ball.coords += (ball.vel * (-TIME_STEP)).astype(int)
                ball.flip_vel(self.parallel, coef_perp=1, coef_par=1)
            elif ball_coords[1] + ball.rad >= wall_coords[1] - self.length / 2 >= ball_coords[1]:
                ball.coords += (ball.vel * (-TIME_STEP)).astype(int)
                ball.flip_vel(self.parallel, coef_perp=1, coef_par=1)
        elif abs(ball_coords[1] - wall_coords[1]) <= self.length / 2:
            if ball_coords[0] - ball.rad <= wall_coords[0] + self.width / 2 <= ball_coords[0]:
                ball.coords += (ball.vel * (-TIME_STEP)).astype(int)
                ball.flip_vel(self.normal, coef_perp=1, coef_par=1)
            elif ball_coords[0] + ball.rad >= wall_coords[0] - self.width / 2 >= ball_coords[0]:
                ball.coords += (ball.vel * (-TIME_STEP)).astype(int)
                ball.flip_vel(self.normal, coef_perp=1, coef_par=1)
        else:
            for vertex in self.vertexes:
                distance = np.linalg.norm(ball.coords - vertex)
                if distance <= ball.rad:
                    ball.coords += (ball.vel * (-TIME_STEP)).astype(int)
                    normal = (ball.coords - vertex) / np.linalg.norm(ball.coords - vertex)
                    ball.flip_vel(normal, coef_perp=1, coef_par=1)


class Manager:
    """
    Manages the process of the game.
    """
    def __init__(self):
        """
        Creates a game: guns, balls, targets and a score table. Creates variables to monitor the state of the game.
        """
        self.gun = Gun()
        self.table = ScoreTable()
        self.balls = []
        self.targets = []
        self.walls = []
        self.done = False
        self.up_key_pressed = False
        self.down_key_pressed = False

    def process(self, events, screen):
        """
        Manages the game. If all the targets have been hit, creates new ones.
        """
        self.handle_events(events)

        if len(self.targets) == 0 and len(self.balls) == 0:
            radius = max(int(30 - self.table.score), 3)
            self.targets = [Target([randint(100, SCREEN_SIZE[0] - 30),
                                    randint(30, SCREEN_SIZE[1] - 30)],
                                   rad=radius) for i in range(3)]
            n = 5 + self.table.score // 10
            self.walls = [Wall(100, 25, coords=[100 + int((SCREEN_SIZE[0] - 200) * (i + 1) / n),
                                                randint(100, SCREEN_SIZE[1] - 100)],
                               angle=randint(-90, 90) * np.pi / 180) for i in range(n)]

        self.check_collisions()
        self.check_alive()
        self.move()
        self.draw(screen)

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
        self.table.draw(screen)
        for wall in self.walls:
            wall.draw(screen)

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
                    self.table.targets_hit += 1

        for wall in self.walls:
            for ball in self.balls:
                wall.collision(ball)

    def handle_events(self, events):
        """
        Handles the events.
        """

        for event in events:
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP or event.key == pg.K_w:
                    self.up_key_pressed = True
                elif event.key == pg.K_DOWN or event.key == pg.K_s:
                    self.down_key_pressed = True
            elif event.type == pg.KEYUP:
                if event.key == pg.K_UP or event.key == pg.K_w:
                    self.up_key_pressed = False
                elif event.key == pg.K_DOWN or event.key == pg.K_s:
                    self.down_key_pressed = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.gun.active = True
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    self.balls.append(self.gun.shoot())
                    self.table.balls_used += 1

        if self.up_key_pressed:
            self.gun.coords[1] = max(10, self.gun.coords[1] - 5)
        if self.down_key_pressed:
            self.gun.coords[1] = min(SCREEN_SIZE[1] - 10, self.gun.coords[1] + 5)

        if pg.mouse.get_focused():
            mouse_pos = pg.mouse.get_pos()
            self.gun.set_angle(mouse_pos)


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

        manager.process(pg.event.get(), screen)
        done = manager.done

        pg.display.update()

    pg.quit()


if __name__ == "__main__":
    main()
