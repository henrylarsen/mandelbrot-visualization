import numpy as np
import matplotlib.pyplot as plt
import time

start = time.time()

min_real = -2.0
max_real = 2.0

min_imaginary = -2.0
max_imaginary = 2.0

number_points_real = 1000
number_points_imaginary = 1000

number_iterations = 100

complex_plane = np.empty([number_points_real, number_points_imaginary], dtype=complex)

# set up complex plane
for j in range(number_points_real):
    for i in range(number_points_imaginary):
        real_component = min_real + (j * (max_real - min_real) / number_points_real)
        imaginary_component = min_imaginary + (i * (max_imaginary - min_imaginary) / number_points_imaginary)
        complex_plane[j, i] = complex(real_component, imaginary_component)


# calculate mandelbrot set
def calculate_mandelbrot(c, max_iterations=number_iterations):
    z = 0
    for _ in range(max_iterations):
        if abs(z) > 2:
            return False
        z = z ** 2 + c
    return True


def calculate_julia(z0, c, max_iterations=number_iterations):
    z = z0
    for _ in range(max_iterations):
        if abs(z) > 10:
            return False
        z = z ** 2 + c
    return True


mapped_plane = np.empty([number_points_real, number_points_imaginary], dtype=bool)
for j in range(number_points_real):
    for i in range(number_points_imaginary):
        # mapped_plane[j, i] = calculate_mandelbrot(complex_plane[j, i])
        mapped_plane[j, i] = calculate_julia(complex_plane[j, i], complex(0.28, 0.008))

for row in range(number_points_real):
    first = mapped_plane[row, 0]
    for column in range(number_points_imaginary):
        if first != mapped_plane[row, column]:
            break

end = time.time()
print(f'compute time: {end - start}')

# Visualize the Mandelbrot set
plt.imshow(mapped_plane, extent=(min_real, max_real, min_imaginary, max_imaginary), cmap="inferno", origin="lower")
plt.colorbar()
plt.title("Mandelbrot Set")
plt.xlabel("Real")
plt.ylabel("Imaginary")
plt.show()

