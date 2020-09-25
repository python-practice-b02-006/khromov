import pygame

PINK = (255, 162, 69)
GREEN = (0, 150, 0)
FPS = 30
W_WIDTH, W_HEIGHT = 640, 480


def draw_tree(surface):
    pass


def draw_panda(surface):
    pass


def main():
    pygame.init()
    screen = pygame.display.set_mode([W_WIDTH, W_HEIGHT])
    pygame.display.set_caption("Pandas")

    clock = pygame.time.Clock()
    finished = False

    while not finished:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True

        screen.fill(PINK)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
