# PROJECTILE MOTION WITH AIR RESISTANCE

import numpy as np
import matplotlib.pyplot as plt


# DEFINING PARAMETERS & INITIAL SPEED

g = 9.81
dt = 0.01
k = 0.01  # Drag coefficient
m = 1  # Mass
total_time = 10

v0 = 50  # Initial speed

angle = 30

max_distance = 0
max_angle = angle


# FINDING THE ANGLE(BETWEEN 30 AND 60 DEGREE) THAT ALLOWS THE OBJECT TO ACHIEVE MAXIMUM HORIZONTAL DISTANCE

for angle in range (30, 61):
    x = 0
    y = 0

    theta = np.radians(angle)

    vx = v0 * np.cos(theta)
    vy = v0 * np.sin(theta)

    t = 0
    v = v0

    while y >= 0:

        ax = -(k/m) * v * vx
        ay = -g-(k/m) * v * vy

        vx = vx + ax * dt
        vy = vy + ay * dt

        v = np.sqrt(vx ** 2 + vy ** 2)

        x = x + vx * dt
        y = y + vy * dt

        t += dt

    final_distance = x

    if final_distance > max_distance:
        max_distance = final_distance
        max_angle = angle

print(f"largest distance is {max_distance:.2f}", "the angle is", max_angle)


# OBTAINING DATA POINTS FOR PLOTTING USING THE MAX ANGLE

x = 0
y = 0
x_list = [x]
y_list = [y]
v0 = 50

theta = np.radians(max_angle)

vx = v0 * np.cos(theta)
vy = v0 * np.sin(theta)

t = 0
v = v0

while y >= 0:
    ax = -(k / m) * v * vx
    ay = -g - (k / m) * v * vy

    vx = vx + ax * dt
    vy = vy + ay * dt

    v = np.sqrt(vx ** 2 + vy ** 2)

    x = x + vx * dt
    y = y + vy * dt

    t += dt

    if y >= 0:
        x_list.append(x)
        y_list.append(y)


# PLOTTING

plt.figure(figsize=(10, 6))
plt.plot(x_list, y_list, label=f'Angle {max_angle}')
plt.title('Projectile Motion with Air Resistance')
plt.xlabel('Distance (m)')
plt.ylabel('Height (m)')
plt.axhline(0, color='black', linestyle='--')
plt.grid(True)
plt.legend()
plt.show()
