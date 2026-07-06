import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from PIL import Image

image_path = "object.png"
img = Image.open("/Users/lamluo/Documents/PythonProjects/BPhO_ComPhys_2025/object.png").convert("RGBA")
object_pixels = np.array(img)

# Real image from a thin lens is inverted.
image_pixels = np.flipud(object_pixels)

f = 1.0
u0 = 2.5

def image_distance(u, f):
    return 1 / (1 / f - 1 / u)

def draw_model(u):
    ax.clear()

    v = image_distance(u, f)
    magnification = -v / u

    object_height = 1.0
    object_width = object_height * object_pixels.shape[1] / object_pixels.shape[0]

    image_height = abs(magnification) * object_height
    image_width = abs(magnification) * object_width

    # Object is on the left of the lens.
    object_x_right = -u
    object_x_left = object_x_right - object_width
    object_bottom = 0
    object_top = object_height

    # Real image is on the right of the lens and inverted.
    image_x_left = v
    image_x_right = v + image_width
    image_bottom = -image_height
    image_top = 0

    ax.imshow(
        object_pixels,
        extent=[object_x_left, object_x_right, object_bottom, object_top],
        origin="upper"
    )

    ax.imshow(
        image_pixels,
        extent=[image_x_left, image_x_right, image_bottom, image_top],
        origin="upper"
    )

    # Lens
    ax.axvline(0, color="black", linewidth=2, label="Thin lens")

    # Optical axis
    ax.axhline(0, color="gray", linewidth=1)

    # Focal points
    ax.scatter([-f, f], [0, 0], color="red", zorder=5, label="Focal points")
    ax.text(-f, -0.15, "-f", ha="center")
    ax.text(f, -0.15, "f", ha="center")

    # Simple principal rays from top of object
    object_top_point = (-u, object_height)
    image_top_point = (v, -image_height)

    # Ray through centre of lens
    ax.plot(
        [object_top_point[0], 0, image_top_point[0]],
        [object_top_point[1], 0, image_top_point[1]],
        color="orange",
        linewidth=1.5
    )

    # Ray parallel to axis then through focal point
    ax.plot(
        [object_top_point[0], 0],
        [object_top_point[1], object_top_point[1]],
        color="green",
        linewidth=1.5
    )
    ax.plot(
        [0, image_top_point[0]],
        [object_top_point[1], image_top_point[1]],
        color="green",
        linewidth=1.5
    )

    ax.set_title(f"Real inverted image: u = {u:.2f}, v = {v:.2f}, magnification = {magnification:.2f}")
    ax.set_xlabel("Distance from lens")
    ax.set_ylabel("Height")
    ax.grid(True)
    ax.legend(loc="upper right")
    ax.set_aspect("equal", adjustable="box")

    x_limit = max(u + object_width + 0.5, v + image_width + 0.5)
    y_limit = max(object_height, image_height) + 0.5

    ax.set_xlim(-x_limit, x_limit)
    ax.set_ylim(-y_limit, y_limit)

    fig.canvas.draw_idle()

fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.22)

slider_ax = plt.axes([0.2, 0.08, 0.6, 0.04])
u_slider = Slider(
    ax=slider_ax,
    label="Object distance u",
    valmin=f + 0.1,
    valmax=5.0,
    valinit=u0
)

def update(val):
    draw_model(u_slider.val)

u_slider.on_changed(update)

draw_model(u0)
plt.show()