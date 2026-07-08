import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


def crown_glass_refractive_index_from_wavelength(lambda_nm):
    x = lambda_nm / 1000
    a = np.array([1.03961212, 0.231792344, 1.01146945])
    b = np.array([0.00600069867, 0.0200179144, 103.560653])

    total = np.zeros_like(x, dtype=float)
    for k in range(len(a)):
        total += (a[k] * x**2) / (x**2 - b[k])

    return np.sqrt(1 + total)


def crown_glass_refractive_index_from_frequency(f_thz):
    lambda_nm = 3.00e8 / (f_thz * 1e12) * 1e9
    return crown_glass_refractive_index_from_wavelength(lambda_nm)


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


def prism_angles(theta_i, alpha, n):
    sin_theta_t = np.sqrt(n**2 - np.sin(theta_i) ** 2) * np.sin(alpha) - np.sin(theta_i) * np.cos(alpha)
    valid = (sin_theta_t >= -1) & (sin_theta_t <= 1)

    theta_t = np.full_like(sin_theta_t, np.nan, dtype=float)
    theta_t[valid] = np.arcsin(sin_theta_t[valid])

    delta = theta_i + theta_t - alpha
    return theta_t, delta, valid


def unit_vector(angle):
    return np.array([np.cos(angle), np.sin(angle)])


def cross_2d(a, b):
    return a[0] * b[1] - a[1] * b[0]


def line_intersection(point, direction, seg_a, seg_b):
    segment_direction = seg_b - seg_a
    denominator = cross_2d(direction, segment_direction)
    if abs(denominator) < 1e-10:
        return None

    t = cross_2d(seg_a - point, segment_direction) / denominator
    u = cross_2d(seg_a - point, direction) / denominator

    if u < 0 or u > 1:
        return None

    return point + t * direction


def prism_vertices(alpha):
    height = 1.6
    half_base = height * np.tan(alpha / 2)
    left = np.array([-half_base, 0.0])
    right = np.array([half_base, 0.0])
    top = np.array([0.0, height])
    return left, right, top


def draw_prism_model(ax, theta_i_deg, alpha_deg):
    ax.clear()

    theta_i = np.radians(theta_i_deg)
    alpha = np.radians(alpha_deg)

    left, right, top = prism_vertices(alpha)
    prism_x = [left[0], top[0], right[0], left[0]]
    prism_y = [left[1], top[1], right[1], left[1]]

    ax.plot(prism_x, prism_y, color="white", linewidth=2)
    ax.fill(prism_x, prism_y, color="black", alpha=0.08)

    entry = left + 0.55 * (top - left)

    normal_left_angle = -alpha / 2
    normal_right_angle = alpha / 2
    incident_direction = unit_vector(normal_left_angle + theta_i)

    ax.plot(
        [entry[0] - 1.4 * incident_direction[0], entry[0]],
        [entry[1] - 1.4 * incident_direction[1], entry[1]],
        color="white",
        linewidth=2.5,
        label="Incident white light",
    )

    frequencies = np.array([442.5, 495, 520, 565, 610, 650, 735])

    for f_thz in frequencies:
        n = crown_glass_refractive_index_from_frequency(f_thz)
        colour = colour_from_frequency(f_thz)

        refracted_angle = np.arcsin(np.sin(theta_i) / n)
        internal_direction = unit_vector(normal_left_angle + refracted_angle)
        exit_point = line_intersection(entry, internal_direction, top, right)

        theta_t, _, valid = prism_angles(
            np.array([theta_i]),
            alpha,
            np.array([n]),
        )

        if exit_point is None or not valid[0]:
            continue

        outgoing_direction = unit_vector(normal_right_angle - theta_t[0])

        ax.plot([entry[0], exit_point[0]], [entry[1], exit_point[1]], color=colour, linewidth=2)
        ax.plot(
            [exit_point[0], exit_point[0] + 1.5 * outgoing_direction[0]],
            [exit_point[1], exit_point[1] + 1.5 * outgoing_direction[1]],
            color=colour,
            linewidth=2,
        )

    ax.text(top[0], top[1] + 0.15, f"alpha = {alpha_deg:.1f} deg", color="white", ha="center")
    ax.text(entry[0] - 0.55, entry[1] + 0.25, f"theta_i = {theta_i_deg:.1f} deg", color="white")

    ax.set_title("Dynamic model of white light through a triangular prism", color="white")
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-2.2, 2.8)
    ax.set_ylim(-1.3, 2.2)
    ax.set_facecolor("black")
    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_color("white")


def plot_theta_t_graph(ax, alpha_deg, f_thz):
    ax.clear()

    alpha = np.radians(alpha_deg)
    n = crown_glass_refractive_index_from_frequency(np.array([f_thz]))[0]
    theta_i_deg = np.linspace(0.01, 89.5, 1000)
    theta_i = np.radians(theta_i_deg)

    theta_t, _, valid = prism_angles(theta_i, alpha, np.full_like(theta_i, n))
    ax.plot(theta_i_deg[valid], np.degrees(theta_t[valid]), color="blue")

    ax.set_xlabel("Angle of incidence / deg")
    ax.set_ylabel("Transmission angle theta_t / deg")
    ax.set_title(f"theta_t vs theta_i, alpha={alpha_deg:.1f} deg, f={f_thz:.1f} THz")
    ax.grid(True)
    ax.set_ylim(0, 100)


def plot_delta_graph(ax, alpha_deg, f_thz):
    ax.clear()

    alpha = np.radians(alpha_deg)
    n = crown_glass_refractive_index_from_frequency(np.array([f_thz]))[0]
    theta_i_deg = np.linspace(0.01, 89.5, 1000)
    theta_i = np.radians(theta_i_deg)

    _, delta, valid = prism_angles(theta_i, alpha, np.full_like(theta_i, n))
    delta_deg = np.degrees(delta)

    ax.plot(theta_i_deg[valid], delta_deg[valid], color="blue")

    if np.any(valid):
        valid_theta = theta_i_deg[valid]
        valid_delta = delta_deg[valid]
        min_index = np.argmin(valid_delta)
        ax.scatter(valid_theta[min_index], valid_delta[min_index], color="red")
        ax.text(
            valid_theta[min_index],
            valid_delta[min_index] + 1.0,
            f"min delta = {valid_delta[min_index]:.2f} deg",
            color="red",
        )

    ax.set_xlabel("Angle of incidence / deg")
    ax.set_ylabel("Deflection angle delta / deg")
    ax.set_title(f"delta vs theta_i, alpha={alpha_deg:.1f} deg, f={f_thz:.1f} THz")
    ax.grid(True)


def plot_dispersion_graph(ax, theta_i_deg, alpha_deg):
    ax.clear()

    theta_i = np.radians(theta_i_deg)
    alpha = np.radians(alpha_deg)
    freq = np.linspace(405, 790, 220)
    n = crown_glass_refractive_index_from_frequency(freq)
    colours = [colour_from_frequency(f) for f in freq]

    _, delta, valid = prism_angles(
        np.full_like(freq, theta_i),
        alpha,
        n,
    )

    ax.scatter(freq[valid], np.degrees(delta[valid]), c=np.array(colours)[valid], s=16)
    ax.set_xlabel("Frequency / THz")
    ax.set_ylabel("Deflection angle delta / deg")
    ax.set_title("Dispersion: deflection of different colours")
    ax.grid(True)


def update(_):
    theta_i_deg = theta_slider.val
    alpha_deg = alpha_slider.val
    f_thz = frequency_slider.val

    draw_prism_model(ax_prism, theta_i_deg, alpha_deg)
    plot_theta_t_graph(ax_theta, alpha_deg, f_thz)
    plot_delta_graph(ax_delta, alpha_deg, f_thz)
    plot_dispersion_graph(ax_dispersion, theta_i_deg, alpha_deg)
    fig.canvas.draw_idle()


fig, ((ax_prism, ax_theta), (ax_delta, ax_dispersion)) = plt.subplots(2, 2, figsize=(13, 9))
plt.subplots_adjust(bottom=0.22, hspace=0.35, wspace=0.3)

theta_slider_ax = plt.axes([0.18, 0.13, 0.65, 0.025])
alpha_slider_ax = plt.axes([0.18, 0.08, 0.65, 0.025])
frequency_slider_ax = plt.axes([0.18, 0.03, 0.65, 0.025])

theta_slider = Slider(theta_slider_ax, "theta_i / deg", 0.5, 80.0, valinit=7.0)
alpha_slider = Slider(alpha_slider_ax, "alpha / deg", 10.0, 80.0, valinit=45.0)
frequency_slider = Slider(frequency_slider_ax, "frequency / THz", 405.0, 790.0, valinit=542.5)

theta_slider.on_changed(update)
alpha_slider.on_changed(update)
frequency_slider.on_changed(update)

update(None)
plt.show()
