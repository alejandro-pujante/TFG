import numpy as np
from calc_sigmas import calc_sigmas


def gauss_func(x, y, z, x0, y0, z0, Q, wind_speed, wind_dir, stability="constant"):
    """
    Shape of the gaussian plume as function of the emission flux or the source,
    wind direction and speed and stability.

    :param x:
    :param y:
    :param z:
    :param x0: x position of the source
    :param y0: y position of the source
    :param z0: z position of the source
    :param Q: emission flux
    :param wind_speed:
    :param wind_dir:
    :param stability:
    :return:
    """

    # Make stack at x0, y0 be the center
    x = x - x0
    y = y - y0
    d = np.sqrt(x ** 2 + y ** 2)  # distance from each point to the center

    wx, wy = wind_speed * np.sin((wind_dir - 180) * np.pi / 180), wind_speed * np.cos((wind_dir - 180) * np.pi / 180)

    # # # Calculate dot product of coordinates and wind to obtain the angle at each point
    dot_product = wx * x + wy * y
    cosine = dot_product / (d * wind_speed)
    sine = np.sqrt(1 - cosine ** 2)

    # # # Calculate the vertical and horizontal components of wind.
    downwind = cosine * d
    crosswind = sine * d

    # # # Indices where downwind > 0
    indx = np.where(downwind > 0.0)

    # # # Shape of the function
    C = np.zeros((x.shape[0], y.shape[1]))
    sigma_y, sigma_z = calc_sigmas(stability, downwind)
    exps = np.exp(-(z[indx] - z0) ** 2 / (2 * sigma_y[indx] ** 2)) + np.exp(
        -(z[indx] + z0) ** 2 / (2 * sigma_y[indx] ** 2))

    C[indx] = Q / (2 * np.pi * wind_speed * sigma_y[indx] * sigma_z[indx]) \
        * np.exp(-crosswind[indx] ** 2 / (2 * sigma_y[indx] ** 2)) \
        * exps

    return C
