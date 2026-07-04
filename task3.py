import numpy as np
import matplotlib.pyplot as plt

L = 2
y = 1
c = 345
n = 1

x = np.linspace(0, L, 500)

AS = np.sqrt(x**2 + y**2)
SB = np.sqrt((L - x)**2 + y**2)
t = (AS + SB) / (c / n)

plt.plot(x, t)
plt.xlabel("x / m")
plt.ylabel("Travel time / s")
plt.title("Fermat principle and reflection")
plt.grid(True)
plt.show()

min_index = np.argmin(t)
x_min = x[min_index]
t_min = t[min_index]

print("Minimum x =", x_min)
print("L/2 =", L / 2)