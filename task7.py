import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from PIL import Image

image_path = "object.png"
img = Image.open("/Users/lamluo/Documents/PythonProjects/BPhO_ComPhys_2025/object.png").convert("RGBA")
object_pixels = np.array(img)

f = 1.0
u0 = 0.6

def image_distance(u, f):
    return 1 / (1 / f - 1 / u)

def draw_model(u):
    ax.clear()

    v = image_distance(u, f)
    magnification = -v / u

    object_height = 1.0
    object_width = object_height * object_pixels.shape[1] / object_pixels.shape[0]

    image_height = magnification * object_height
    image_width = magnification * object_width

    # Object is on the left of the lens.
    object_x_right = -u
    object_x_left = object_x_right - object_width
    object_bottom = 0
    object_top = object_height

    # For u < f, v is negative, so the virtual image is also on the left.
    image_x_right = v
    image_x_left = image_x_right - image_width
    image_bottom = 0
    image_top = image_height

    ax.imshow(
        object_pixels,
        extent=[object_x_left, object_x_right, object_bottom, object_top],
        origin="upper"
    )

    ax.imshow(
        object_pixels,
        extent=[image_x_left, image_x_right, image_bottom, image_top],
        origin="upper",
        alpha=0.55
    )

    # Lens
    ax.axvline(0, color="black", linewidth=2, label="Thin lens")

    # Optical axis
    ax.axhline(0, color="gray", linewidth=1)

    # Focal points
    ax.scatter([-f, f], [0, 0], color="red", zorder=5, label="Focal points")
    ax.text(-f, -0.15, "-f", ha="center")
    ax.text(f, -0.15, "f", ha="center")

    object_top_point = (-u, object_height)
    virtual_top_point = (v, image_height)

    # Ray through centre of lens: appears to come from virtual image.
    ax.plot(
        [object_top_point[0], 0],
        [object_top_point[1], 0],
        color="orange",
        linewidth=1.5
    )
    ax.plot(
        [virtual_top_point[0], 0],
        [virtual_top_point[1], 0],
        color="orange",
        linestyle="--",
        linewidth=1.2
    )

    # Ray parallel to axis, refracted as if from the left focal point.
    ax.plot(
        [object_top_point[0], 0],
        [object_top_point[1], object_top_point[1]],
        color="green",
        linewidth=1.5
    )
    ax.plot(
        [0, 2.0],
        [object_top_point[1], object_top_point[1] - 2.0 * object_top_point[1] / f],
        color="green",
        linewidth=1.5
    )
    ax.plot(
        [virtual_top_point[0], 0],
        [virtual_top_point[1], object_top_point[1]],
        color="green",
        linestyle="--",
        linewidth=1.2
    )

    ax.set_title(f"Virtual enlarged image: u = {u:.2f}, v = {v:.2f}, magnification = {magnification:.2f}")
    ax.set_xlabel("Distance from lens")
    ax.set_ylabel("Height")
    ax.grid(True)
    ax.legend(loc="upper right")
    ax.set_aspect("equal", adjustable="box")

    left_limit = min(image_x_left - 0.5, object_x_left - 0.5, -2.5)
    right_limit = 2.5
    y_limit = max(image_height, object_height) + 0.5

    ax.set_xlim(left_limit, right_limit)
    ax.set_ylim(-0.8, y_limit)

    fig.canvas.draw_idle()

fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.22)

slider_ax = plt.axes([0.2, 0.08, 0.6, 0.04])
u_slider = Slider(
    ax=slider_ax,
    label="Object distance u",
    valmin=0.2,
    valmax=f - 0.05,
    valinit=u0
)

def update(val):
    draw_model(u_slider.val)

u_slider.on_changed(update)

draw_model(u0)
plt.show()