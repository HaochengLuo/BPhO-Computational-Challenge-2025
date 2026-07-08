import numpy as np
import matplotlib.pyplot as plt


def water_refractive_index(f_thz):
    f_hz = f_thz * 1e12
    A = 1.731 - 0.261 * (f_hz / 1e15) ** 2
    return np.sqrt(1 + np.sqrt(1 / A))


def colour_from_frequency(f_thz):
    if f_thz < 480:
        return (1.0, 0.0, 0.0)
    if f_thz < 510:
        return (1.0, 127 / 255, 0.0)
    if f_thz < 530:
        return (1.0, 1.0, 0.0)
    if f_thz < 600:
        return (0.0, 1.0, 0.0)
    if f_thz < 620:
        return (0.0, 1.0, 1.0)
    if f_thz < 680:
        return (0.0, 0.0, 1.0)
    return (127 / 255, 0.0, 1.0)


def primary_elevation(theta, n):
    refraction_angle = np.arcsin(np.sin(theta) / n)
    return 4 * refraction_angle - 2 * theta


def secondary_elevation(theta, n):
    refraction_angle = np.arcsin(np.sin(theta) / n)
    return np.pi - 6 * refraction_angle + 2 * theta


def primary_extreme_theta(n):
    return np.arcsin(np.sqrt((4 - n**2) / 3))


def secondary_extreme_theta(n):
    return np.arcsin(np.sqrt((9 - n**2) / 8))


def plot_elevation_vs_theta():
    theta_deg = np.linspace(0.01, 89.9, 1200)
    theta = np.radians(theta_deg)

    frequencies = np.array([442.5, 495, 520, 565, 610, 650, 735])
    colour_names = ["Red", "Orange", "Yellow", "Green", "Cyan", "Blue", "Violet"]

    fig, ax = plt.subplots(figsize=(10, 6))

    for f_thz, name in zip(frequencies, colour_names):
        n = water_refractive_index(f_thz)
        colour = colour_from_frequency(f_thz)

        primary = np.degrees(primary_elevation(theta, n))
        secondary = np.degrees(secondary_elevation(theta, n))

        theta_primary = primary_extreme_theta(n)
        theta_secondary = secondary_extreme_theta(n)
        epsilon_primary = np.degrees(primary_elevation(theta_primary, n))
        epsilon_secondary = np.degrees(secondary_elevation(theta_secondary, n))

        ax.plot(theta_deg, primary, color=colour, linewidth=2, label=f"Primary {name}")
        ax.plot(theta_deg, secondary, color=colour, linestyle="--", linewidth=2, label=f"Secondary {name}")
        ax.scatter(np.degrees(theta_primary), epsilon_primary, color=colour, edgecolor="black", s=30)
        ax.scatter(np.degrees(theta_secondary), epsilon_secondary, color=colour, edgecolor="black", s=30)

    ax.set_xlabel("Angle of incidence theta / deg")
    ax.set_ylabel("Rainbow elevation epsilon / deg")
    ax.set_title("Descartes rainbow model: elevation vs incidence angle")
    ax.set_xlim(0, 90)
    ax.set_ylim(0, 180)
    ax.grid(True)
    ax.legend(fontsize=8, ncol=2)


def plot_elevation_vs_frequency():
    freq = np.linspace(405, 790, 386)
    n = water_refractive_index(freq)
    colours = [colour_from_frequency(f) for f in freq]

    theta_primary = primary_extreme_theta(n)
    theta_secondary = secondary_extreme_theta(n)

    epsilon_primary = np.degrees(primary_elevation(theta_primary, n))
    epsilon_secondary = np.degrees(secondary_elevation(theta_secondary, n))

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(freq, epsilon_primary, c=colours, s=18, label="Primary rainbow")
    ax.scatter(freq, epsilon_secondary, c=colours, s=18, marker="x", label="Secondary rainbow")

    ax.set_xlabel("Frequency / THz")
    ax.set_ylabel("Rainbow elevation epsilon / deg")
    ax.set_title("Primary and secondary rainbow elevation vs frequency")
    ax.set_ylim(40, 54)
    ax.grid(True)
    ax.legend()

    print("Primary rainbow angle range:", np.min(epsilon_primary), "to", np.max(epsilon_primary), "deg")
    print("Secondary rainbow angle range:", np.min(epsilon_secondary), "to", np.max(epsilon_secondary), "deg")


plot_elevation_vs_theta()
plot_elevation_vs_frequency()
plt.show()
