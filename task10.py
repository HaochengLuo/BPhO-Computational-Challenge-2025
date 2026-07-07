import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from PIL import Image

image_path = "object.png"

img = Image.open("/Users/lamluo/Documents/PythonProjects/BPhO_ComPhys_2025/object.png").convert("RGBA")
img.thumbnail((180, 180))
pixels = np.array(img)

height, width, _ = pixels.shape
rows, cols = np.indices((height, width))

colors = pixels.reshape(-1, 4) / 255
alpha = colors[:, 3]

# Convert pixel coordinates to mathematical coordinates.
# The image is fitted into a unit circle.
x_unit = (cols - width / 2) / (width / 2)
y_unit = (height / 2 - rows) / (height / 2)

x_flat = x_unit.reshape(-1)
y_flat = y_unit.reshape(-1)
colors_flat = colors

# Keep only visible pixels inside the unit circle.
inside_circle = (x_flat**2 + y_flat**2 <= 1) & (colors_flat[:, 3] > 0.05)

x_flat = x_flat[inside_circle]
y_flat = y_flat[inside_circle]
colors_flat = colors_flat[inside_circle]


def anamorphic_map(x, y, Rf, arc_degrees):
    # x controls angular position around the cylinder.
    # y controls radial distance from the base point.
    theta_max = np.radians(arc_degrees / 2)

    theta = x * theta_max
    radius = Rf - y

    X = radius * np.sin(theta)
    Y = -radius * np.cos(theta)

    return X, Y


def draw_model(Rf, arc_degrees):
    ax_object.clear()
    ax_anamorphic.clear()

    X, Y = anamorphic_map(x_flat, y_flat, Rf, arc_degrees)

    # Original fitted image in unit circle
    circle = plt.Circle((0, 0), 1, fill=False, color="black", linewidth=2)
    ax_object.add_patch(circle)
    ax_object.scatter(x_flat, y_flat, c=colors_flat, s=6, marker="s")

    ax_object.axhline(0, color="gray", linewidth=1)
    ax_object.axvline(0, color="gray", linewidth=1)
    ax_object.scatter([0], [-1], color="red", s=70, marker="*", label="Base point")

    ax_object.set_title("Object fitted into unit circle")
    ax_object.set_xlabel("x")
    ax_object.set_ylabel("y")
    ax_object.grid(True)
    ax_object.legend(loc="upper right")
    ax_object.set_aspect("equal")
    ax_object.set_xlim(-1.2, 1.2)
    ax_object.set_ylim(-1.2, 1.2)

    # Anamorphic mapped image
    ax_anamorphic.scatter(X, Y, c=colors_flat, s=6, marker="s")

    theta_max = np.radians(arc_degrees / 2)
    theta_line = np.linspace(-theta_max, theta_max, 300)

    for r in [Rf - 1, Rf, Rf + 1]:
        arc_x = r * np.sin(theta_line)
        arc_y = -r * np.cos(theta_line)
        ax_anamorphic.plot(arc_x, arc_y, color="gray", linewidth=0.8, alpha=0.6)

    ax_anamorphic.scatter([0], [0], color="red", s=70, marker="*", label="Base point")
    ax_anamorphic.axhline(0, color="gray", linewidth=1)
    ax_anamorphic.axvline(0, color="gray", linewidth=1)

    ax_anamorphic.set_title("Anamorphic image for cylindrical mirror")
    ax_anamorphic.set_xlabel("X")
    ax_anamorphic.set_ylabel("Y")
    ax_anamorphic.grid(True)
    ax_anamorphic.legend(loc="upper right")
    ax_anamorphic.set_aspect("equal")

    max_radius = Rf + 1.3
    ax_anamorphic.set_xlim(-max_radius, max_radius)
    ax_anamorphic.set_ylim(-max_radius - 0.5, 0.8)

    fig.canvas.draw_idle()


fig, (ax_object, ax_anamorphic) = plt.subplots(1, 2, figsize=(12, 6))
plt.subplots_adjust(bottom=0.22)

rf_slider_ax = plt.axes([0.2, 0.11, 0.6, 0.03])
arc_slider_ax = plt.axes([0.2, 0.05, 0.6, 0.03])

rf_slider = Slider(
    rf_slider_ax,
    "Rf",
    1.5,
    6.0,
    valinit=3.0
)

arc_slider = Slider(
    arc_slider_ax,
    "Arc angle / degrees",
    60,
    220,
    valinit=160
)


def update(_):
    draw_model(rf_slider.val, arc_slider.val)


rf_slider.on_changed(update)
arc_slider.on_changed(update)

draw_model(rf_slider.val, arc_slider.val)

plt.show()