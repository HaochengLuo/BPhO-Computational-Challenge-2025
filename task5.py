import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

image_path = "object.png"
img = Image.open("/Users/lamluo/Documents/PythonProjects/BPhO_ComPhys_2025/object.png").convert("RGBA")
object_pixels = np.array(img)

height, width, channels = object_pixels.shape

# Flip image horizontally for the virtual image
virtual_pixels = np.fliplr(object_pixels)

# Scale image so it fits nicely on coordinate axes
scale = 100
image_width = width / scale
image_height = height / scale

# Object is placed to the right of the mirror x = 0
object_left = 1
object_right = object_left + image_width
object_bottom = -image_height / 2
object_top = image_height / 2

# Virtual image is the mirror reflection in x = 0
virtual_left = -object_right
virtual_right = -object_left
virtual_bottom = object_bottom
virtual_top = object_top

fig, ax = plt.subplots(figsize=(9, 6))

# Plot original object
ax.imshow(
    object_pixels,
    extent=[object_left, object_right, object_bottom, object_top],
    origin="upper"
)

# Plot virtual image
ax.imshow(
    virtual_pixels,
    extent=[virtual_left, virtual_right, virtual_bottom, virtual_top],
    origin="upper"
)

# Mirror line
ax.axvline(0, color="black", linewidth=2, label="Plane mirror")

# Coordinate axes
ax.axhline(0, color="gray", linewidth=1)
ax.axvline(0, color="black", linewidth=2)

# Grid and labels
ax.grid(True)
ax.set_xlabel("x coordinate")
ax.set_ylabel("y coordinate")
ax.set_title("Virtual image in a plane mirror")

ax.set_aspect("equal")
ax.set_xlim(virtual_left - 1, object_right + 1)
ax.set_ylim(object_bottom - 1, object_top + 1)

ax.legend()
plt.show()