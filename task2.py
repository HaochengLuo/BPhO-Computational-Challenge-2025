import numpy as np
import matplotlib.pyplot as plt

# given data points
u = np.array([20, 25, 30, 35, 40, 45, 50, 55])
v = np.array([65.5, 40, 31, 27, 25, 23.1, 21.5, 20.5])

x = 1 / u
y = 1 / v

# plot the data points
plt.grid(True)
plt.scatter(x, y, color="blue")
plt.xlabel("1/u")
plt.ylabel("1/v")
plt.title("Thin lens")

# line of best fit
m, b = np.polyfit(x, y, 1)
plt.plot(x, m * x + b, color="red", linewidth=2, label="Best Fit Line")
plt.legend()
plt.show()

# print focal length
f = 1 / b

print("Gradient =", m)
print("Intercept =", b)
print("Focal length =", f, "cm")