import numpy as np
import matplotlib.pyplot as plt

L = 2
y = 1
Y = 1

c1 = 345
c2 = 230

x = np.linspace(0, L, 500)

AS = np.sqrt(x**2 + y**2)
SB = np.sqrt((L - x)**2 + Y**2)
t = AS / c1 + SB / c2

min_index = np.argmin(t)
x_min = x[min_index]
t_min = t[min_index]

AS_min = np.sqrt(x_min**2 + y**2)
SB_min = np.sqrt((L - x_min)**2 + Y**2)

sin_theta = x_min / AS_min
sin_phi = (L - x_min) / SB_min

print("Minimum x =", x_min)
print("Minimum travel time =", t_min)
print("sin(theta)/c1 =", sin_theta / c1)
print("sin(phi)/c2 =", sin_phi / c2)

plt.plot(x, t)
plt.scatter(x_min, t_min, color="red", label="Minimum time")
plt.xlabel("x / m")
plt.ylabel("Travel time / s")
plt.title("Fermat principle and refraction")
plt.grid(True)
plt.legend()
plt.show()