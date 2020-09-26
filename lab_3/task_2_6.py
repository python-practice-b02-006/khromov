import pygame
import numpy as np

PINK = (255, 175, 128)
GREEN = (0, 104, 55)
FPS = 30
W_WIDTH, W_HEIGHT = 640, 480


def draw_branch(surface, left_dir, start_angle, stop_angle, num_leaves, rect):
    width, height = surface.get_width(), surface.get_height()
    branch = pygame.Surface((rect[2], rect[3]))
    branch.fill(PINK)

    for i in range(num_leaves):
        leave = pygame.Surface((int(width / 9), int(height / 30)))
        leave.fill(PINK)
        pygame.draw.ellipse(leave, GREEN, ((0, 0), (int(width / 9), int(height / 30))))
        leave = pygame.transform.rotate(leave, 100)

        angle = start_angle + i * np.pi / 8
        x = int(np.sign(np.tan(angle)) * ((rect[2] / 2)**(-2) + (np.tan(angle) / (rect[3] / 2)) ** 2) ** (-0.5))
        y = - int(x * np.tan(angle))
        x += int(rect[2] / 2)
        y += int(rect[3] / 2)
        branch.blit(leave, (x, y))

    pygame.draw.arc(branch, GREEN, ((0, 0), (rect[2], rect[3])), start_angle, stop_angle, 3)

    if left_dir:
        branch = pygame.transform.flip(branch, 1, 0)

    surface.blit(branch, (rect[0], rect[1]))


def draw_trunk(surface):
    width, height = surface.get_width(), surface.get_height()

    # two bottom rectangles
    pygame.draw.rect(surface, GREEN, (int(width / 2 - width / 40), int(3 * height / 4),
                                      int(width / 20), int(height / 5)))
    pygame.draw.rect(surface, GREEN, (int(width / 2 - width / 40), int(2 * height / 4),
                                      int(width / 20), int(height / 4.5)))

    # second to top rectangle
    rotated_rect_1 = pygame.Surface((int(width / 20), int(height / 5.5)))
    rotated_rect_1.fill(PINK)
    pygame.draw.line(rotated_rect_1, GREEN,
                     (int(width / 40), int(0.1 * height / 12)),
                     (int(width / 40), int(2.1 * height / 12)),
                     int(width / 20))
    rotated_rect_1 = pygame.transform.rotate(rotated_rect_1, - 10)
    surface.blit(rotated_rect_1, (int(width / 2 - width / 40), int(1.2 * height / 4)))

    # top rectangle
    rotated_rect_2 = pygame.Surface((int(width / 30), int(height / 4)))
    rotated_rect_2.fill(PINK)
    pygame.draw.line(rotated_rect_2, GREEN,
                     (int(width / 60), 0),
                     (int(width / 60), int(height / 4)),
                     int(width / 30))
    rotated_rect_2 = pygame.transform.rotate(rotated_rect_2, - 20)
    surface.blit(rotated_rect_2, (int(width / 2 + width / 90), int(0.2 * height / 4)))


def draw_tree(surface):
    surface.fill(PINK)
    width, height = surface.get_width(), surface.get_height()

    draw_trunk(surface)

    # right branches
    draw_branch(surface, False, np.pi / 2.5, np.pi, 4, (int(width / 2 + width / 10), int(0.8 * height / 4),
                                                        int(width / 2), int(height / 4)))
    draw_branch(surface, False, np.pi / 3, np.pi, 3, (int(width / 2 + width / 30), int(1.7 * height / 4),
                                                      int(width / 3), int(height / 4)))
    # left branches
    draw_branch(surface, True, np.pi / 3, np.pi, 3, (int(width / 2 - 11 * width / 30), int(1.6 * height / 4),
                                                     int(width / 3), int(height / 4)))
    draw_branch(surface, True, np.pi / 2.5, np.pi, 4, (int(width / 2 - 8 * width / 15), int(0.6 * height / 4),
                                                       int(width / 2), int(height / 4)))


def draw_panda(surface):
    pass


def main():
    pygame.init()
    screen = pygame.display.set_mode([W_WIDTH, W_HEIGHT])
    pygame.display.set_caption("Pandas")

    clock = pygame.time.Clock()
    finished = False

    screen.fill(PINK)

    while not finished:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True

        tree_1 = pygame.Surface((int(W_WIDTH / 2), int(W_HEIGHT / 1.5)), pygame.SRCALPHA)
        draw_tree(tree_1)
        screen.blit(tree_1, (int(W_WIDTH / 3.6), 0))

        tree_2 = pygame.Surface((int(W_WIDTH / 2.6), int(W_HEIGHT / 2)), pygame.SRCALPHA)
        draw_tree(tree_2)
        screen.blit(tree_2, (-int(W_WIDTH / 20), int(W_HEIGHT / 10)))

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
