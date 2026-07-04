import numpy as np
import matplotlib.pyplot as plt

RI = []

# Range of wavelength
wavelength = np.linspace(400, 800, 401)

# Convert from nm to um
x = wavelength/1000

# Sellmeier coefficients
a = [1.03961212, 0.231792344, 1.01146945]
b = [0.00600069867, 0.0200179144, 103.560653]

# Sellmeier formula
for i in range(len(wavelength)):
    total = 0
    lam = x[i]

    for j in range(0, 3):
        total += (a[j] * lam**2)/(lam**2 - b[j])

    n = np.sqrt(1 + total)

    RI.append(n)

RI = np.array(RI)

# plotting
plt.plot(wavelength, RI)
plt.grid(True)
plt.xlabel("Wavelength / nm")
plt.ylabel("Refractive index")
plt.title("Refractive index of BK7 crown glass")
plt.show()

