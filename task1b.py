import numpy as np
import matplotlib.pyplot as plt

# freq of light
freq = np.linspace(405, 790, 386)
freqHz = freq*(10**12)

RI = []

# formula to calculate n
for i in range(len(freq)):
    n = np.sqrt(np.sqrt(1/(1.731-0.261*(freqHz[i]/(10**15))**2)) + 1)

    RI.append(n)

RI = np.array(RI)

# plotting
plt.plot(freq, RI)
plt.grid(True)
plt.xlabel("Frequency / THz")
plt.ylabel("Refractive index")
plt.title("Refractive index of water")
plt.show()
