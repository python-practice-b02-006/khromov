import pygame
import numpy as np

PEACH = (255, 175, 128)
GREEN = (0, 104, 55)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 30
W_WIDTH, W_HEIGHT = 800, 600


def draw_branch(surface, left_dir, start_angle, stop_angle, num_leaves, rect):
    """Draws a branch of the tree.

    :param surface: surface on which the tree is being drawn.
    :param left_dir: by default the branch is drawn facing right. If the parameter is True, it is reflected
     relative to the vertical axes.
    :param start_angle: branch is drawn as an arc of an ellipse. This is the start angle of the arc.
    :param stop_angle:  branch is drawn as an arc of an ellipse. This is the end angle of the arc.
    :param num_leaves: number of leaves growing on the branch.
    :param rect: based on rect a separate surface is created for the branch. The surface is then attached via
     blit() method to the main surface.
    :return: None.
    """
    width, height = surface.get_width(), surface.get_height()
    branch = pygame.Surface((rect[2], rect[3]))
    branch.fill(PEACH)
    branch.set_colorkey(PEACH)

    for i in range(num_leaves):
        leave = pygame.Surface((int(height / 8), int(width / 36)))
        leave.fill(PEACH)
        leave.set_colorkey(PEACH)
        pygame.draw.ellipse(leave, GREEN, ((0, 0), (int(height / 8), int(width / 35))))
        leave = pygame.transform.rotate(leave, 100)

        angle = start_angle + i * np.pi / 10
        x = np.sign(np.tan(angle)) * ((rect[2] / 2)**(-2) + (np.tan(angle) / (rect[3] / 2)) ** 2) ** (-0.5)
        y = - x * np.tan(angle)
        x += rect[2] / 2
        y += rect[3] / 2
        x = int(x)
        y = int(y)
        branch.blit(leave, (x, y))

    pygame.draw.arc(branch, GREEN, ((0, 0), (rect[2], rect[3])), start_angle, stop_angle, 3)

    if left_dir:
        branch = pygame.transform.flip(branch, 1, 0)

    surface.blit(branch, (rect[0], rect[1]))


def draw_trunk(surface):
    """Draws the trunk of the tree.

    :param surface: surface on which the tree is being drawn.
    :return: None.
    """
    width, height = surface.get_width(), surface.get_height()

    # two bottom rectangles
    pygame.draw.rect(surface, GREEN, (int(width / 2 - width / 40), int(3 * height / 4),
                                      int(width / 20), int(height / 5))
                     )
    pygame.draw.rect(surface, GREEN, (int(width / 2 - width / 40), int(2 * height / 4),
                                      int(width / 20), int(height / 4.5))
                     )

    # second to top rectangle
    rotated_rect_1 = pygame.Surface((int(width / 20), int(height / 5.5)))
    rotated_rect_1.fill(PEACH)
    rotated_rect_1.set_colorkey(PEACH)
    pygame.draw.line(rotated_rect_1, GREEN,
                     (int(width / 40), int(0.1 * height / 12)),
                     (int(width / 40), int(2.1 * height / 12)),
                     int(width / 20)
                     )
    rotated_rect_1 = pygame.transform.rotate(rotated_rect_1, - 10)
    surface.blit(rotated_rect_1, (int(width / 2 - width / 40), int(1.2 * height / 4)))

    # top rectangle
    rotated_rect_2 = pygame.Surface((int(width / 30), int(height / 4)))
    rotated_rect_2.fill(PEACH)
    rotated_rect_2.set_colorkey(PEACH)
    pygame.draw.line(rotated_rect_2, GREEN,
                     (int(width / 60), 0),
                     (int(width / 60), int(height / 4)),
                     int(width / 30)
                     )
    rotated_rect_2 = pygame.transform.rotate(rotated_rect_2, - 20)
    surface.blit(rotated_rect_2, (int(width / 2 + width / 90), int(0.2 * height / 4)))


def draw_tree(surface):
    """Draws a tree.

    :param surface: the tree is drawn on the surface.
    :return: None.
    """
    surface.fill(PEACH)
    surface.set_colorkey(PEACH)
    width, height = surface.get_width(), surface.get_height()

    draw_trunk(surface)

    # right branches
    draw_branch(surface, False, np.pi / 2.5, np.pi, 5, (int(width / 2 + width / 10), int(0.8 * height / 4),
                                                        int(width / 2), int(height / 4))
                )
    draw_branch(surface, False, np.pi / 3, np.pi, 3, (int(width / 2 + width / 30), int(1.7 * height / 4),
                                                      int(width / 3), int(height / 4))
                )
    # left branches
    draw_branch(surface, True, np.pi / 3, np.pi, 3, (int(width / 2 - 11 * width / 30), int(1.6 * height / 4),
                                                     int(width / 3), int(height / 4))
                )
    draw_branch(surface, True, np.pi / 2.5, np.pi, 5, (int(width / 2 - 8 * width / 15), int(0.6 * height / 4),
                                                       int(width / 2), int(height / 4))
                )


def draw_body(surface, rect):
    """Draws the body of the panda.

    :param surface: surface on which the panda is being drawn.
    :param rect: rectangle, containing the body.
    :return: None
    """
    pygame.draw.ellipse(surface, WHITE, rect)


def draw_rightmost_leg(surface, rect):
    """Draws the rightmost leg of the panda.

    :param surface: surface on which the panda is being drawn.
    :param rect: rectangle, containing the leg.
    :return: None
    """
    width, height = rect[2], rect[3]
    points = [
        (int(rect[0] + width * 0.75), int(rect[1] + height * 0.05)),
        (int(rect[0] + width * 0.7), int(rect[1] + height * 0.5)),
        (int(rect[0] + width * 0.55), int(rect[1] + height * 0.8)),
        (int(rect[0] + width * 0.35), int(rect[1] + height * 0.95)),
        (int(rect[0] + width * 0.2), int(rect[1] + height * 0.98)),
        (rect[0], int(rect[1] + height * 0.8)),
        (int(rect[0] + width * 0.55), int(rect[1] + height * 0.05)),
        (int(rect[0] + width * 0.65), rect[1])
    ]
    pygame.draw.polygon(surface, BLACK, points)

    pygame.draw.ellipse(surface, BLACK, (int(rect[0] - width * 0.1), int(rect[1] + height * 0.7),
                                         int(width * 0.5), int(height * 0.3))
                        )


def draw_middle_leg(surface, rect):
    """Draws the middle leg of the panda.

    :param surface: surface on which the panda is being drawn.
    :param rect: rectangle, containing the leg.
    :return: None
    """
    width, height = rect[2], rect[3]
    points = [
        (int(rect[0] + width * 0.9), int(rect[1] + height * 0.05)),
        (int(rect[0] + width * 0.95), int(rect[1] + height * 0.6)),
        (int(rect[0] + width * 0.8), int(rect[1] + height * 0.85)),
        (int(rect[0] + width * 0.5), int(rect[1] + height * 0.93)),
        (int(rect[0] + width * 0.25), int(rect[1] + height * 0.85)),
        (int(rect[0] + width * 0.6), int(rect[1] + height * 0.5)),
        (int(rect[0] + width * 0.7), rect[1])
    ]
    pygame.draw.polygon(surface, BLACK, points)

    pygame.draw.ellipse(surface, BLACK, (int(rect[0] + width * 0.2), int(rect[1] + height * 0.7),
                                         int(width * 0.5), int(height * 0.23))
                        )


def draw_leftmost_leg(surface, rect):
    """Draws the leftmost leg of the panda.

    :param surface: surface on which the panda is being drawn.
    :param rect: rectangle, containing the leg.
    :return: None
    """
    width, height = rect[2], rect[3]
    points = [
        (int(rect[0] + width * 0.25), rect[1]),
        (int(rect[0] + width * 0.07), int(rect[1] + height * 0.5)),
        (rect[0], int(rect[1] + height * 0.8)),
        (int(rect[0] + width * 0.25), int(rect[1] + height * 0.95)),
        (int(rect[0] + width * 0.5), int(rect[1] + height * 0.99)),
        (int(rect[0] + width * 0.75), int(rect[1] + height * 0.75)),
        (int(rect[0] + width * 0.65), int(rect[1] + height * 0.5)),
        (int(rect[0] + width * 0.5), rect[1])
    ]
    pygame.draw.polygon(surface, BLACK, points)

    pygame.draw.ellipse(surface, BLACK, (int(rect[0] + height * 0.06), int(rect[1] + height * 0.7),
                                         int(width * 0.85), int(height * 0.3))
                        )


def draw_head(surface, rect):
    """Draws the head of the panda.

    :param surface: surface on which the panda is being drawn.
    :param rect: rectangle, containing the head.
    :return: None
    """
    width, height = rect[2], rect[3]

    # ears
    pygame.draw.circle(surface, BLACK, (int(rect[0] + width * 0.28), int(rect[0] + height * 0.23)),
                       int(height * 0.2)
                       )
    pygame.draw.circle(surface, BLACK, (int(rect[0] + width * 0.77), int(rect[0] + height * 0.33)),
                       int(height * 0.23)
                       )
    points = [
        (int(rect[0] + width * 0.15), int(rect[1] + height / 3)),
        (int(rect[0] + width * 0.25), int(rect[1] + height / 6)),
        (int(rect[0] + width * 0.35), int(rect[1] + height / 14)),
        (int(rect[0] + width * 0.5), int(rect[1] + height * 0.02)),
        (int(rect[0] + width * 0.6), int(rect[1] + height * 0.02)),
        (int(rect[0] + width * 0.75), int(rect[1] + height / 10)),
        (int(rect[0] + width * 0.8), int(rect[1] + height / 2)),
        (int(rect[0] + width * 0.85), int(rect[1] + height / 1.9)),
        (int(rect[0] + width * 0.9), int(rect[1] + height / 2)),
        (int(rect[0] + width * 0.9), int(rect[1] + 2.3 * height / 3)),
        (int(rect[0] + width * 0.85), int(rect[1] + 2.6 * height / 3)),
        (int(rect[0] + width * 0.45), rect[1] + height),
        (int(rect[0] + width * 0.35), rect[1] + height),
        (int(rect[0] + width * 0.17), int(rect[1] + 2.5 * height / 3))
    ]
    pygame.draw.polygon(surface, WHITE, points)

    # nose
    pygame.draw.ellipse(surface, BLACK, (int(rect[0] + width * 0.15), int(rect[1] + height * 0.85),
                                         int(width * 0.25), int(height * 0.2))
                        )
    # eyes
    pygame.draw.ellipse(surface, BLACK, (int(rect[0] + width * 0.13), int(rect[1] + height / 2),
                                         int(width * 0.17), int(height * 0.25))
                        )
    pygame.draw.ellipse(surface, BLACK, (int(rect[0] + width * 0.4), int(rect[1] + height / 1.8),
                                         int(height * 0.25), int(height * 0.25))
                        )


def draw_panda(surface):
    """ Draws panda.

    :param surface: the panda is drawn on the surface.
    :return: None.
    """
    surface.fill(PEACH)
    surface.set_colorkey(PEACH)
    width, height = surface.get_width(), surface.get_height()

    draw_body(surface, (int(width / 10), int(height / 5),
                        int(width / 1.2), int(height / 2.2))
              )
    draw_rightmost_leg(surface, (int(width / 1.55), int(9 * height / 20),
                                 int(width / 2.8), int(10 * height / 20))
                       )
    draw_middle_leg(surface, (int(width * 0.25), int(height / 5.5),
                              int(width / 2.7), int(height * 0.85))
                    )
    draw_leftmost_leg(surface, (int(width * 0.05), int(1.5 * height / 5),
                                int(width / 3.5), int(height * 0.6))
                      )
    draw_head(surface, (0, 0,
                        int(width / 1.65), int(height * 0.6))
              )


def main():
    """The main function of the program.

    :return: None
    """
    pygame.init()
    screen = pygame.display.set_mode([W_WIDTH, W_HEIGHT])
    pygame.display.set_caption("Pandas")

    clock = pygame.time.Clock()
    finished = False

    screen.fill(PEACH)

    while not finished:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True

        tree_1 = pygame.Surface((int(W_WIDTH / 2), int(W_HEIGHT / 1.5)))
        draw_tree(tree_1)
        screen.blit(tree_1, (int(W_WIDTH / 3.6), 0))

        tree_2 = pygame.Surface((int(W_WIDTH / 3.5), int(W_HEIGHT / 2)))
        draw_tree(tree_2)
        screen.blit(tree_2, (int(W_WIDTH / 5.8), int(W_HEIGHT / 7)))

        panda_1 = pygame.Surface((int(W_WIDTH / 3.2), int(W_HEIGHT / 2.5)))
        draw_panda(panda_1)
        screen.blit(panda_1, (int(1.8 * W_WIDTH / 3), int(W_HEIGHT / 2.5)))

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
