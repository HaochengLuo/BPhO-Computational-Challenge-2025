import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from PIL import Image

image_path = "object.png"

img = Image.open("/Users/lamluo/Documents/PythonProjects/BPhO_ComPhys_2025/object.png").convert("RGBA")
img.thumbnail((140, 140))
pixels = np.array(img)

height, width, _ = pixels.shape
rows, cols = np.indices((height, width))

colors = pixels.reshape(-1, 4) / 255
alpha = colors[:, 3]
visible = alpha > 0.05

rows_flat = rows.reshape(-1)[visible]
cols_flat = cols.reshape(-1)[visible]
colors = colors[visible]


def convex_mirror_map(x_obj, y_obj, R):
    y_safe = np.where(np.abs(y_obj) < 1e-6, 1e-6, y_obj)

    alpha = 0.5 * np.arctan(y_safe / x_obj)
    k = x_obj / np.cos(2 * alpha)

    denominator = k / R - np.cos(alpha) + (x_obj / y_safe) * np.sin(alpha)
    valid = np.abs(denominator) > 1e-8

    y_img = (k * np.sin(alpha)) / denominator
    x_img = x_obj * y_img / y_safe

    return x_img, y_img, valid


def draw_model(object_distance, object_height, R):
    ax.clear()

    object_width = object_height * width / height

    x_obj = object_distance + (cols_flat - width / 2) / width * object_width
    y_obj = (height / 2 - rows_flat) / height * object_height

    x_img, y_img, valid = convex_mirror_map(x_obj, y_obj, R)

    mirror_y = np.linspace(-R, R, 500)
    mirror_x = R - np.sqrt(R**2 - mirror_y**2)

    ax.plot(mirror_x, mirror_y, color="black", linewidth=3, label="Convex mirror")
    ax.axhline(0, color="gray", linewidth=1)
    ax.axvline(0, color="lightgray", linewidth=1)

    ax.scatter([0], [0], color="black", s=30)
    ax.text(0, -0.08, "mirror vertex", ha="center")

    ax.scatter([R / 2], [0], color="red", s=40)
    ax.text(R / 2, -0.08, "F", ha="center", color="red")

    ax.scatter([R], [0], color="purple", s=40)
    ax.text(R, -0.08, "C", ha="center", color="purple")

    ax.scatter(x_obj, y_obj, c=colors, s=5, marker="s", label="Object")
    ax.scatter(
        x_img[valid],
        y_img[valid],
        c=colors[valid],
        s=5,
        marker="s",
        alpha=0.75,
        label="Virtual image"
    )

    # Example ray from top of object
    point_x = object_distance
    point_y = object_height / 2

    ray_x_img, ray_y_img, ray_valid = convex_mirror_map(
        np.array([point_x]),
        np.array([point_y]),
        R
    )

    if ray_valid[0]:
        image_point_x = ray_x_img[0]
        image_point_y = ray_y_img[0]

        hit_y = point_y * 0.5
        hit_x = R - np.sqrt(R**2 - hit_y**2)

        ax.plot([point_x, hit_x], [point_y, hit_y], color="green", linewidth=1.5)
        ax.plot([hit_x, point_x + 0.8], [hit_y, hit_y - 0.4], color="green", linewidth=1.5)

        ax.plot(
            [image_point_x, hit_x],
            [image_point_y, hit_y],
            color="green",
            linestyle="--",
            linewidth=1.2
        )

    ax.set_title(
        f"Virtual image in a convex spherical mirror: R = {R:.2f}, object distance = {object_distance:.2f}"
    )
    ax.set_xlabel("x coordinate")
    ax.set_ylabel("y coordinate")
    ax.grid(True)
    ax.legend(loc="upper right")
    ax.set_aspect("equal", adjustable="box")

    right_limit = max(object_distance + object_width + 0.5, R + 0.5)
    ax.set_xlim(-0.3, right_limit)

    y_limit = max(R, object_height) + 0.3
    ax.set_ylim(-y_limit, y_limit)

    fig.canvas.draw_idle()


fig, ax = plt.subplots(figsize=(10, 7))
plt.subplots_adjust(bottom=0.28)

object_distance_slider_ax = plt.axes([0.2, 0.17, 0.6, 0.03])
object_height_slider_ax = plt.axes([0.2, 0.11, 0.6, 0.03])
radius_slider_ax = plt.axes([0.2, 0.05, 0.6, 0.03])

object_distance_slider = Slider(
    object_distance_slider_ax,
    "Object distance",
    0.4,
    1.8,
    valinit=0.9
)

object_height_slider = Slider(
    object_height_slider_ax,
    "Object height",
    0.15,
    0.8,
    valinit=0.45
)

radius_slider = Slider(
    radius_slider_ax,
    "Mirror radius R",
    0.6,
    1.5,
    valinit=1.0
)


def update(_):
    draw_model(
        object_distance_slider.val,
        object_height_slider.val,
        radius_slider.val
    )


object_distance_slider.on_changed(update)
object_height_slider.on_changed(update)
radius_slider.on_changed(update)

draw_model(
    object_distance_slider.val,
    object_height_slider.val,
    radius_slider.val
)

plt.show()