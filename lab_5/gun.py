import pygame

FPS = 30
W_WIDTH, W_HEIGHT = 800, 600
BLACK = (0, 0, 0)
TIME_STEP = 0.01
GRAVITY = 10


class Ball:
    def __init__(self):
        pass

    def move(self):
        pass

    def collide(self):
        pass

    def draw(self, screen):
        pass


class Target:
    def __init__(self):
        pass

    def collide(self):
        pass

    def draw(self, screen):
        pass

    def move(self):
        pass


class Gun:
    def __init__(self):
        pass

    def turn_on(self):
        pass

    def gain_power(self):
        pass

    def target(self, event):
        pass

    def shoot(self):
        pass

    def move(self):
        pass

    def draw(self, screen):
        pass


class ScoreTable:
    def __init__(self):
        pass

    def draw(self, screen):
        pass


class Manager:
    def __init__(self, n_targets=1):
        self.targets = [Target() for i in range(n_targets)]
        self.gun = Gun()
        self.balls = []

    def process(self, screen):
        done = self.handle_events()

        self.move()
        self.collide()
        self.draw(screen)

        return done

    def handle_events(self):
        done = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        return done

    def move(self):
        for ball in self.balls:
            ball.move()
        for target in self.targets:
            target.move()

    def draw(self, screen):
        screen.fill(BLACK)

        for ball in self.balls:
            ball.draw(screen)
        for target in self.targets:
            target.draw(screen)
        self.gun.draw(screen)

    def collide(self):
        for ball in self.balls:
            ball.collide()
        for target in self.targets:
            target.collide()


def main():
    pygame.init()
    screen = pygame.display.set_mode((W_WIDTH, W_HEIGHT))

    pygame.display.update()
    clock = pygame.time.Clock()

    done = False

    manager = Manager()
    while not done:
        clock.tick(FPS)

        done = manager.process(screen)

    pygame.quit()


if __name__ == "__main__":
    main()
