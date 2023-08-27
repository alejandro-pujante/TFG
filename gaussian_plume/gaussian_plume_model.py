import numpy as np
from gauss_func import gauss_func


def create_space(xlims, ylims, zlims, **kwargs):  # Cambiar para que devuelve x, y, z con shape=(Nx, Ny)
    x = np.mgrid[xlims[0]: xlims[1]: kwargs["dx"]]
    y = np.mgrid[ylims[0]: ylims[1]: kwargs["dy"]]
    z = np.mgrid[zlims[0]: zlims[1]: kwargs["dz"]]
    return x, y, z


class GaussianModel:
    def __init__(self, xlims, ylims, zlims, tlims, runmode, **kwargs):
        """
        Initialize model.

        :param xlims:
        :param ylims:
        :param zlims:
        :param tlims:
        :param runmode:
        :param kwargs: {"dxi": dxi}
        """
        self.runmode = runmode
        self.x, self.y, self.z = self.set_space(xlims, ylims, zlims, **kwargs)
        self.t = self.set_time(tlims, **kwargs)

    def set_space(self, xlims, ylims, zlims, **kwargs):
        """
        Sets up the grid. Only modes implemented are "plan" and "hslice".

        :param xlims:
        :param ylims:
        :param zlims:
        :param kwargs: "dx", "dy", "dz"

        :return: grid
        """

        x, y, _ = create_space(xlims, ylims, zlims, **kwargs)
        x, y = np.meshgrid(x, y)
        z = np.zeros(x.shape)

        if self.runmode == "plan":
            pass

        elif self.runmode == "hslice":
            _, y, z = create_space(xlims, ylims, zlims, **kwargs)
            y, z = np.meshgrid(y, z)
            x = kwargs["x_value"] * np.ones(z.shape)

        else:
            print(f"Runmode {self.runmode} not available, try 'plan' or 'hslice'.")

        return x, y, z

    @staticmethod
    def set_time(tlims, **kwargs):
        """
        Set the time values for the solution.

        :param tlims: lower/upper time limits
        :param kwargs: "dt"

        :return: array of times
        """
        return np.mgrid[tlims[0]: tlims[1]: kwargs["dt"]]

    def set_conditions(self, stability: dict, wind: dict):
        """
        Stability and wind conditions of simulation.

        :param stability: {"condition": __, "value": __}
        :param wind: {"condition": __, "speed": __, "direction": __}

        :return: stability and wind for each time in the calculation.
        """
        # # # Stability conditions
        if stability["condition"] == "constant":
            stab = stability["value"] * np.ones(len(self.t))
        else:
            stab = stability["value"] * np.ones(len(self.t))
            print("Not supported stability conditions " + stability["condition"])

        # # # Wind conditions
        if wind["condition"] == "constant":
            wind_speed = wind["speed"] * np.ones(len(self.t))
            wind_dir = wind["direction"] * np.ones(len(self.t))
        else:
            wind_speed = wind["speed"] * np.ones(len(self.t))
            wind_dir = wind["direction"] * np.ones(len(self.t))
            print("Not supported wind conditions " + wind['condition'])

        return stab, wind_speed, wind_dir

    def set_shape(self):
        if self.runmode == "plan":
            shape = (self.x.shape[1], self.y.shape[0], len(self.t))
        else:
            shape = (self.y.shape[1], self.z.shape[0], len(self.t))

        return shape

    def solve(self, Q, stacks, stability, wind):
        """Solves the concentrations for each time and point in the domain

        Args:
            Q (_type_): _description_
            stacks (_type_): _description_
            stability (_type_): _description_
            wind (_type_): _description_

        Returns:
            _type_: _description_
        """
        # # # Set time space
        shape = self.set_shape()

        # # # Set stability and wind conditions
        stability, wind_speed, wind_dir = self.set_conditions(stability, wind)

        # # # Calculation of solution
        C = np.zeros(shape=shape)

        # Loop for each time index
        for (i, speed_i), dir_i, stab in zip(enumerate(wind_speed), wind_dir, stability):
            # Loop for each source
            for (x0, y0, z0), Qi in zip(stacks, Q):
                C[:, :, i] += gauss_func(
                    self.x, self.y, self.z, x0, y0, z0,
                    Qi, speed_i, dir_i, stability=stab
                )

        return C
