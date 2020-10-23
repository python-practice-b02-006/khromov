import pygame
import numpy as np

FPS = 30
W_WIDTH, W_HEIGHT = 800, 600

BLACK = (0, 0, 0)
RED = (255, 0, 0)

TIME_STEP = 0.01
GRAVITY = 10


class Ball:
    pass


class Target:
    pass


class Gun:
    def __init__(self):
        self.coords = [30, W_HEIGHT // 2]
        self.angle = 0

    def draw(self, screen):
        end_pos = [int(self.coords[0] + 20 * np.cos(self.angle)),
                   int(self.coords[1] + 20 * np.sin(self.angle))]
        pygame.draw.line(screen, RED, self.coords, end_pos, 5)

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

    def process(self, events, screen):
        done = self.handle_events(events)
        self.draw(screen)
        return done

    def draw(self, screen):
        screen.fill(BLACK)
        self.gun.draw(screen)

    def handle_events(self, events):
        done = False
        for event in events:
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.gun.coords[1] -= 5
                elif event.key == pygame.K_DOWN:
                    self.gun.coords[1] += 5

        if pygame.mouse.get_focused():
            mouse_pos = pygame.mouse.get_pos()
            self.gun.set_angle(mouse_pos)

        return done


def main():
    pygame.init()
    screen = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
    clock = pygame.time.Clock()

    done = False

    manager = Manager()
    while not done:
        clock.tick(FPS)

        done = manager.process(pygame.event.get(), screen)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
