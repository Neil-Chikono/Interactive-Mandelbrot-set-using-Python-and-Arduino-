#viewing a mandelbrot fractal through a python program


#z_{n+1}=z_n^2+c
import matplotlib
matplotlib.use("MacOSX")
import math


import numpy as np 
import matplotlib.pyplot as plt 


#zoom parameters 

zoom = 1.0 
center_x = -0.5
center_y = 0.0

def mandelbrot(width, height, zoom, center_x, center_y, max_iterations ):
    
#calaulate the visible region 
    scale = 1.5 / zoom 

    x_min = center_x - scale 
    x_max = center_x + scale 

    y_min = center_y - scale 
    y_max = center_y + scale 

    # create corordinates 

    x = np.linspace(x_min, x_max,  width)
    y = np.linspace(y_min, y_max, height)

    #create a grid of complex numbers 
    c = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    # initalaize Z 

    Z = np.zeros_like(c)

    #store sthe escape iteration for each pixel 
    result = np.full(c.shape, max_iterations)

    #track points that have not escaped 
    active = np.ones(c.shape, dtype=bool)

    for i in range(max_iterations):

    #mandelbot equation 

        Z[active] = np.cos(Z)[active] ** 7 + np.sin(c) [active]

        #find points that have escaped 
        escaped = active & (np.abs(Z) > 2)

        #recodr thier iteration 
        result[escaped] = i 

        #calculating escaped points 
        active[escaped] = False

    return result


# Generate the fractal


import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Connect to Arduino

arduino = serial.Serial(
    "/dev/cu.usbmodem143201",
    115200,
    timeout=0
)

# Fractal parameters

width = 400
height = 400
max_iterations = 100

zoom = 1.0
center_x = -0.5
center_y = 0.0

# Create the initial fractal

fig, ax = plt.subplots()

fractal = mandelbrot(
    width,
    height,
    zoom,
    center_x,
    center_y,
    max_iterations
)

image = ax.imshow(
    fractal,
    cmap="inferno",
    origin="lower",
    vmin=0,
    vmax=max_iterations
)

ax.axis("off")

# Store incoming serial data

buffer = ""
previous_values = None


def update(frame):

    global buffer
    global zoom, center_x
    global previous_values

    # Read available Arduino data

    incoming = arduino.read(
        arduino.in_waiting
    ).decode("utf-8", errors="ignore")

    buffer += incoming

    # Separate complete lines

    lines = buffer.split("\n")

    buffer = lines[-1]

    # Find the latest valid reading

    for line in reversed(lines[:-1]):

        try:
            pot1, pot2 = map(
                int, line.strip().split(",")
            )

            if not (
                0 <= pot1 <= 1023
                and 0 <= pot2 <= 1023
            ):
                continue

        except ValueError:
            continue

        # Avoid unnecessary recalculations

        if previous_values is not None:

            old1, old2 = previous_values

            if (
                abs(pot1 - old1) < 3
                and abs(pot2 - old2) < 3
            ):
                return image,

        previous_values = (pot1, pot2)

        # Map potentiometer values

        zoom = 1 + (pot1 / 1023) * 99

        center_x = -2 + (pot2 / 1023) * 3

        # Recalculate fractal

        fractal = mandelbrot(
            width,
            height,
            zoom,
            center_x,
            center_y,
            max_iterations
        )

        # Update the existing image

        image.set_data(fractal)

        ax.set_title(
            f"Zoom: {zoom:.2f}x | "
            f"X: {center_x:.3f}"
        )

        break

    return image,


# Continuously update the image

animation = FuncAnimation(
    fig,
    update,
    interval=50,
    cache_frame_data=False
)

try:
    plt.show()

finally:
    arduino.close()
