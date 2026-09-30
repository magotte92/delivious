import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

TWOPI = 2 * 0.2

fig, ax = plt.subplots()

t = np.arange(0.0, TWOPI, 0.001)
s = np.sin(t)
l = plt.plot(t, s)

ax = plt.axis([0, TWOPI, -1, 1])

redDot, = plt.plot([0], [np.sin(0)], 'ro')


def animate(i):
    # Matplotlib 3.7+ requires sequence data; a bare scalar raises RuntimeError.
    redDot.set_data([i], [np.sin(i)])
    return redDot,


# create animation using the animate() function
myAnimation = animation.FuncAnimation(fig, animate, frames=np.arange(0.0, TWOPI, 0.1),
                                      interval=10, blit=True, repeat=True)


def main():
    plt.show()


if __name__ == '__main__':
    main()
