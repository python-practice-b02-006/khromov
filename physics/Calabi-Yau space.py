import matplotlib.pyplot as plt
import numpy as np
import matplotlib.tri as mtri


def z1(theta, xi, n, k):
    return np.exp(2 * np.pi * 1j * k / n) * (np.cos(xi + theta * 1j)) ** (2 / n)


def z2(theta, xi, n, k):
    return np.exp(2 * np.pi * 1j * k / n) * (np.sin(xi + theta * 1j)) ** (2 / n)


def calculate_points(n1, n2, xi_steps, theta_steps, xi_max, angle):
    patch = np.zeros((n2, n1, xi_steps + 2, theta_steps + 2, 4), dtype=float)

    max_color = -np.inf
    for k2 in range(n2):
        for k1 in range(n1):
            xi_num = 0
            for xi in np.arange(- xi_max, xi_max + 2 * xi_max / xi_steps,
                                2 * xi_max / xi_steps):
                theta_num = 0
                for theta in np.arange(0, np.pi / 2 + np.pi / (2 * theta_steps),
                                       np.pi / (2 * theta_steps)):
                    x = np.real(z1(theta, xi, n1, k1))
                    y = np.real(z2(theta, xi, n2, k2))
                    z = np.cos(angle) * np.imag(z1(theta, xi, n1, k1)) + \
                        np.sin(angle) * np.imag(z2(theta, xi, n2, k2))
                    color = np.sin(angle) * np.imag(z1(theta, xi, n1, k1)) - \
                            np.cos(angle) * np.imag(z2(theta, xi, n2, k2))
                    if abs(color) > max_color:
                        max_color = abs(color)
                    patch[k2][k1][xi_num][theta_num] = [x, y, z, color]

                    theta_num += 1

                xi_num += 1

    return patch, max_color


def draw_manifold(n1, n2, xi_steps, theta_steps, patch, max_color):
    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection='3d')

    colors = [[255, 255, 0], [65, 105, 225], [255, 69, 0], [34, 139, 34], [255, 165, 0], [0, 255, 255]]

    for k2 in range(n2):
        for k1 in range(n1):
            for xi_num in range(xi_steps):
                for theta_num in range(theta_steps):
                    x_1 = [patch[k2][k1][xi_num][theta_num][0]] + \
                          [patch[k2][k1][xi_num][theta_num + 1][0]] + \
                          [patch[k2][k1][xi_num + 1][theta_num][0]]
                    x_2 = [patch[k2][k1][xi_num][theta_num + 1][0]] + \
                          [patch[k2][k1][xi_num + 1][theta_num + 1][0]] + \
                          [patch[k2][k1][xi_num + 1][theta_num][0]]

                    y_1 = [patch[k2][k1][xi_num][theta_num][1]] + \
                          [patch[k2][k1][xi_num][theta_num + 1][1]] + \
                          [patch[k2][k1][xi_num + 1][theta_num][1]]
                    y_2 = [patch[k2][k1][xi_num][theta_num + 1][1]] + \
                          [patch[k2][k1][xi_num + 1][theta_num + 1][1]] + \
                          [patch[k2][k1][xi_num + 1][theta_num][1]]

                    z_1 = [patch[k2][k1][xi_num][theta_num][2]] + \
                          [patch[k2][k1][xi_num][theta_num + 1][2]] + \
                          [patch[k2][k1][xi_num + 1][theta_num][2]]
                    z_2 = [patch[k2][k1][xi_num][theta_num + 1][2]] + \
                          [patch[k2][k1][xi_num + 1][theta_num + 1][2]] + \
                          [patch[k2][k1][xi_num + 1][theta_num][2]]

                    color_1 = ((patch[k2][k1][xi_num][theta_num][3] +
                                patch[k2][k1][xi_num][theta_num + 1][3] +
                                patch[k2][k1][xi_num + 1][theta_num][3]) / 3)
                    color_1 = 1 - abs(color_1 / max_color)
                    color_1 = np.array(colors[k1*k2 % len(colors)]) * color_1 / 255

                    color_2 = ((patch[k2][k1][xi_num + 1][theta_num + 1][3] +
                                patch[k2][k1][xi_num][theta_num + 1][3] +
                                patch[k2][k1][xi_num + 1][theta_num][3]) / 3)
                    color_2 = 1 - abs(color_2 / max_color)
                    color_2 = np.array(colors[k1*k2 % len(colors)]) * color_2 / 255

                    triangle_1 = mtri.Triangulation(x_1, y_1)
                    triangle_2 = mtri.Triangulation(x_2, y_2)

                    ax1.plot_trisurf(triangle_1, z_1, color=color_1, shade=False)
                    ax1.plot_trisurf(triangle_2, z_2, color=color_2, shade=False)

    plt.show()


def main():
    n1, n2 = 6, 6

    # Doesn't work for n1 = 4 or n2 = 4, presumably because some triangles are vertical.
    # Works for n1, n2 = 2, 3, 5, 6, 7, 8. Should work for other values, but I didn't check.

    xi_steps, xi_max = 12, np.pi / 2
    theta_steps = 10
    angle = np.pi / 4

    patch, max_color = calculate_points(n1, n2, xi_steps, theta_steps, xi_max, angle)

    draw_manifold(n1, n2, xi_steps, theta_steps, patch, max_color)


if __name__ == "__main__":
    main()
