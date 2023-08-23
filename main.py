import numpy as np
import matplotlib.pyplot as plt
import time
import struct
from mpmath import *

start = time.time()

min_real = -2.0
max_real = 2.0

min_imaginary = -2.0
max_imaginary = 2.0

number_points_real = 500
number_points_imaginary = 500

zoom_factor = 0.1

iterations = 1000


def setup_plane(min_r, max_r, min_i, max_i):
    # complex_plane = np.empty([number_points_real, number_points_imaginary], dtype=complex)

    real = np.linspace(min_real, max_real, number_points_real)
    imaginary = np.linspace(min_imaginary, max_imaginary, number_points_imaginary)
    X, Y = np.meshgrid(real, imaginary)
    complex_plane = X + 1j * Y
    return complex_plane


"""
    # set up complex plane
    for j in range(number_points_real):
        for i in range(number_points_imaginary):
            real_component = min_r + (j * (max_r - min_r) / number_points_real)
            # print(f'real_component: {real_component}')
            imaginary_component = min_i + (i * (max_i - min_i) / number_points_imaginary)
            # print(f'imaginary_component: {imaginary_component}')
            complex_plane[j, i] = mpc(real_component, imaginary_component)

    # print(f'complex_plane: {complex_plane[0][0]}, {complex_plane[499][499]} ')
"""


# calculate mandelbrot set
def calculate_mandelbrot(c, max_iterations=iterations):
    z = 0
    for _ in range(max_iterations):
        if abs(z) > 2:
            return False
        z = z ** 2 + c
    return True


def calculate_julia(z0, c, max_iterations=iterations):
    z = z0
    for _ in range(max_iterations):
        if abs(z) > 10:
            return False
        z = z ** 2 + c
    return True


def plot_mandelbrot(x_min, x_max, y_min, y_max):

    complex_plane = setup_plane(x_min, x_max, y_min, y_max)
    elements_still_in_set = np.ones((number_points_real, number_points_imaginary), dtype=bool)
    elements_mapped = np.zeros((number_points_real, number_points_imaginary), dtype=complex)

    for iteration in range(iterations):
        elements_mapped[elements_still_in_set] = elements_mapped[elements_still_in_set]**2 + \
                                                 complex_plane[elements_still_in_set]
        mask = np.logical_and(np.absolute(elements_mapped) > 2, elements_still_in_set)
    #     Add a pixel grid here if looking for other more than boolean values with pixel_grid
        elements_still_in_set = np.logical_and(elements_still_in_set, np.logical_not(mask))



    # pixel_grid = np.zeros((number_points_real, number_points_imaginary, 3), dtype=np.uint8)
    #
    # complex_plane = setup_plane(x_min, x_max, y_min, y_max)
    # mapped_plane = np.zeros_like(complex_plane)
    # # print(f'mapped_plane: {mapped_plane}')
    # elements_todo = np.ones((number_points_real, number_points_imaginary), dtype=bool)
    # for iteration in range(iterations):
    #     mapped_plane[elements_todo] = mapped_plane[elements_todo] ** 2 + complex_plane[elements_todo]
    #     mask = np.logical_and(np.absolute(mapped_plane) > 2, elements_todo)
    #     pixel_grid[mask, :] = (iteration, iteration, iteration)
    #     elements_todo = np.logical_and(elements_todo, np.logical_not(mask))

    # for j in range(number_points_real):
    #     for i in range(number_points_imaginary):
    #         mapped_plane[j, i] = calculate_mandelbrot(complex_plane[i, j])
            # mapped_plane[j, i] = calculate_julia(complex_plane[j, i], complex(0.28, 0.008))

    # Visualize the Mandelbrot set
    end = time.time()
    print(f'compute time: {end - start}')
    plt.imshow(elements_still_in_set, extent=(x_min, x_max, y_min, y_max), cmap="inferno", origin="lower")
    plt.colorbar()
    plt.title("Mandelbrot Set")
    plt.xlabel("Real")
    plt.ylabel("Imaginary")


def plot_mandelbrot2(x_min, x_max, y_min, y_max):
    real_axis = np.linspace(min_real, max_real, num=number_points_real)
    imaginary_axis = np.linspace(min_imaginary, max_imaginary, num=number_points_imaginary)

    complex_grid_np = np.zeros((number_points_real, number_points_imaginary), dtype=complex)
    real, imag = np.meshgrid(real_axis, imaginary_axis)
    complex_grid_np.real = real
    complex_grid_np.imag = imag



def zoom(event):
    global min_real, max_real, min_imaginary, max_imaginary

    plt.clf()
    # Mouse coordinates
    x, y = event.xdata, event.ydata

    new_width = (max_real - min_real) * zoom_factor
    new_height = (max_imaginary - min_imaginary) * zoom_factor

    # new coordinates
    new_xmin = x - new_width / 2
    new_xmax = x + new_width / 2
    new_ymin = y - new_height / 2
    new_ymax = y + new_height / 2

    min_real, max_real, min_imaginary, max_imaginary = new_xmin, new_xmax, new_ymin, new_ymax

    print(f'{new_xmin}, {new_xmax}, {new_ymin}, {new_ymax}')

    plot_mandelbrot(new_xmin, new_xmax, new_ymin, new_ymax)
    plt.draw()


# Show the initial plot
plot_mandelbrot(min_real, max_real, min_imaginary, max_imaginary)

# plt.connect('button_press_event', zoom)
plt.show()


