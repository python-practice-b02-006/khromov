import numpy as np
import matplotlib.pyplot as plt

MAX_TIME = 500
X0, Y0, Z0 = 10, 10, 10
DELTA_T = 0.01

# A, B, C = 10, 0.5, 8/3
# A, B, C = 10, 10, 8/3
# A, B, C = 10, 18, 8/3
# A, B, C = 10, 24.06, 8/3
A, B, C = 10, 28, 8/3


def update_coords(r, time):
    r_now = r[:, time - 1]
    v_x = A * (r_now[1] - r_now[0])
    v_y = r_now[0] * (B - r_now[2]) - r_now[1]
    v_z = r_now[0] * r_now[1] - C * r_now[2]

    r[:, time] = [r_now[0] + DELTA_T * v_x,
                  r_now[1] + DELTA_T * v_y,
                  r_now[2] + DELTA_T * v_z
                  ]
    return r


def main():
    r = np.zeros((3, MAX_TIME))
    r[:, 0] = [X0, Y0, Z0]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    plt.ion()
    line = ax.plot(r[0, :1], r[1, :1], r[2, :1], color='blue')[0]

    print("Simulation started")
    for time in range(1, MAX_TIME):
        r = update_coords(r, time)
        line.set_data_3d(r[0, :time+1], r[1, :time+1], r[2, :time+1])

        ax.set_xlim(min(r[0, :]) - 5, max(r[0, :]) + 5)
        ax.set_ylim(min(r[1, :]) - 5, max(r[1, :]) + 5)
        ax.set_zlim(min(r[2, :]) - 5, max(r[2, :]) + 5)

        plt.gcf().canvas.flush_events()
        plt.show()

    print("Simulation finished")
    plt.ioff()
    plt.show()


if __name__ == "__main__":
    main()
