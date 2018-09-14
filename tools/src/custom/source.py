#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from modules.base import StellarSource

"""Add your defined classes to this dictionary with a unique name
 to use it with PolarisTools.
"""
def update_sources_dict(dictionary):
    sources_dict = {
        'f_type': FType,
        'gg_tau_stars': GGTauStars,
        'hd97048': HD97048,
        'line': Line,
        'custom': CustomStar,
    }
    dictionary.update(sources_dict)


class CustomStar(StellarSource):
    """Change this to the star you want to use.
    """

    def __init__(self, file_io, parse_args):
        """Initialisation of the stellar source parameters.

        Args:
            file_io : Handles file input/output and all necessary paths.
        """
        StellarSource.__init__(self, file_io, parse_args)

        # Position of the star [m, m, m]
        self.parameter['position'] = [0, 0, 0]
        # Effective temperature of the star [K]
        self.parameter['temperature'] = 4000
        # Radius of the star [R_sun] or luminosity [L_sun]
        self.parameter['radius'] = 2.0 * self.math.const['R_sun']
        # Number of photons if no number is chosen via --photons
        self.parameter['nr_photons'] = 1000000
        # Can the velocity field be calculated by only this star in the center?
        self.parameter['kepler_usable'] = True
        # Mass of the star [M_sun] (for Keplerian rotation)
        self.parameter['mass'] = 0.7 * self.math.const['M_sun']

    def get_command(self):
        """Provides stellar source command line for POLARIS .cmd file.

        Returns:
            str: Command line to consider the stellar source.
        """
        '''To add multiple stars, use the following:
        new_command_line = str()
        self.parameter['temperature'] = 8000
        self.parameter['radius'] = 4.0 * self.math.const['R_sun']
        new_command_line += self.get_command_line()
        self.parameter['temperature'] = 5000
        self.parameter['radius'] = 3.0 * self.math.const['R_sun']
        new_command_line += self.get_command_line()
        return new_command_line
        '''
        return self.get_command_line()


class FType(StellarSource):
    """Change this to the star you want to use.
    """

    def __init__(self, file_io, parse_args):
        """Initialisation of the stellar source parameters.

        Args:
            file_io : Handles file input/output and all necessary paths.
        """
        StellarSource.__init__(self, file_io, parse_args)

        # Position of the star [m, m, m]
        self.parameter['position'] = [0, 0, 0]
        # Effective temperature of the star [K]
        self.parameter['temperature'] = 6500
        # Radius of the star [R_sun]
        self.parameter['radius'] = 1.3 * self.math.const['R_sun']
        # Mass of the star [M_sun] (for Keplerian rotation)
        self.parameter['mass'] = 0.7 * self.math.const['M_sun']
        # Number of photons if no number is chosen via --photons
        self.parameter['nr_photons'] = 1000000


class GGTauStars(StellarSource):
    """The BinaryStar class is three pre-main sequence stars in the center
    and a planet in the disk.
    """

    def __init__(self, file_io, parse_args):
        """Initialisation of the stellar source parameters.

        Args:
            file_io : Handles file input/output and all
                necessary paths.

        Notes:
            - White et. al 1999 (separation of components, luminosity)
                "http://iopscience.iop.org/article/10.1086/307494/pdf"
            - Correia et. al 2008 (stellar temperature/spectral type)
                "https://arxiv.org/pdf/astro-ph/0608674.pdf"

        """
        StellarSource.__init__(self, file_io, parse_args)

        self.parameter['nr_photons'] = 100000

        a_Aab = 36. / 2.
        a_Ab12 = 4.5 / 2.
        a_planet = 260. + 20.

        angle_Aa = 3. / 2. * np.pi
        angle_Ab = angle_Aa + np.pi
        angle_planet = np.pi * (360. - 127.) / 180.

        '''
        From Robert Brunngräber!
        1 million years
        1 M_jup:  T = 839.9 K, L = 1.409e-5 L_sun
        10 M_jup: T = 2423 K,  L = 1.950e-3 L_sun

        10 millionen years
        1 M_jup:  T = 528.7 K, L = 1.423e-6 L_sun
        10 M_jup: T = 1591 K,  L = 1.262e-4 L_sun

        Accreting circumplanetary disks: observational signatures (Zhu 2015)
        # print(self.math.planet_lum(5.683e26, 1e-8, 58232e3))
        # Saturn like star -> L = 5.37e-4 L_sun
        #                  -> T = 4000 K

        '''

        #: dict: Parameters for the binary components
        self.parameter_lst = {
            # New: M0, M2, M3 (http://www.pas.rochester.edu/~emamajek/EEM_dwarf_UBVIJHK_colors_Teff.txt)
            'temperature': [3870., 3550., 3410., 839.9],
            'luminosity': np.multiply([0.84, 0.40, 0.31, 1e-1 * (1.4e-5 + 1.863234318727217e-3)],
                                      self.mathm.const['L_sun']),
            'position_star': [[0., a_Aab * self.math.const['au'] * np.sin(angle_Aa), 0.],
                              [a_Aab * self.math.const['au'] * np.cos(angle_Ab) + a_Ab12 * self.math.const['au'],
                               a_Aab * self.math.const['au'] * np.sin(angle_Ab), 0.],
                              [a_Aab * self.math.const['au'] * np.cos(angle_Ab) - a_Ab12 * self.math.const['au'],
                               a_Aab * self.math.const['au'] * np.sin(angle_Ab), 0.],
                              [a_planet * self.math.const['au'] * np.sin(angle_planet),
                               a_planet * self.math.const['au'] * np.cos(angle_planet), 0.],
                              ]
        }

    def get_command(self):
        new_command_line = str()
        for i_comp in range(len(self.parameter_lst['temperature'])):
            self.parameter['temperature'] = self.parameter_lst['temperature'][i_comp]
            self.parameter['luminosity'] = self.parameter_lst['luminosity'][i_comp]
            self.parameter['position'] = self.parameter_lst['position_star'][i_comp]
            new_command_line += self.get_command_line()
        return new_command_line


class HD97048(StellarSource):
    """Change this to the star you want to use.
    """

    def __init__(self, file_io, parse_args):
        """Initialisation of the stellar source parameters.

        Args:
            file_io : Handles file input/output and all necessary paths.
        """
        StellarSource.__init__(self, file_io, parse_args)

        # Position of the star [m, m, m]
        self.parameter['position'] = [0, 0, 0]
        # Effective temperature of the star [K]
        self.parameter['temperature'] = 10000
        # Radius of the star [R_sun]
        self.parameter['radius'] = 2.0 * self.math.const['R_sun']
        # Mass of the star [M_sun] (for Keplerian rotation)
        self.parameter['mass'] = 1.0 * self.math.const['M_sun']
        # Number of photons if no number is chosen via --photons
        self.parameter['nr_photons'] = 1000000

class Line(StellarSource):
    """A line of stars
    """

    def __init__(self, file_io, parse_args):
        """Initialisation of the stellar source parameters.

        Args:
            file_io : Handles file input/output and all necessary paths.
        """
        StellarSource.__init__(self, file_io, parse_args)

        # Effective temperature of the star [K]
        self.parameter['temperature'] = 4000
        # Radius of the star [R_sun]
        self.parameter['radius'] = 0.9 * self.math.const['R_sun']
        # Mass of the star [M_sun] (for Keplerian rotation)
        self.parameter['mass'] = 0.7 * self.math.const['M_sun']
        # Number of photons if no number is chosen via --photons
        self.parameter['nr_photons'] = 1e5

    def get_command(self):
        new_command_line = str()
        self.parameter['position'] = [0, 0, 0]
        new_command_line += self.get_command_line()
        self.parameter['position'] = [0, 0, 10 * self.math.const['au']]
        new_command_line += self.get_command_line()
        self.parameter['position'] = [0, 0, -10 * self.math.const['au']]
        new_command_line += self.get_command_line()
        self.parameter['position'] = [0, 0, 20 * self.math.const['au']]
        new_command_line += self.get_command_line()
        self.parameter['position'] = [0, 0, -20 * self.math.const['au']]
        new_command_line += self.get_command_line()
        self.parameter['position'] = [0, 0, 30 * self.math.const['au']]
        new_command_line += self.get_command_line()
        self.parameter['position'] = [0, 0, -30 * self.math.const['au']]
        new_command_line += self.get_command_line()
        self.parameter['position'] = [0, 0, 40 * self.math.const['au']]
        new_command_line += self.get_command_line()
        self.parameter['position'] = [0, 0, -40 * self.math.const['au']]
        new_command_line += self.get_command_line()
        self.parameter['position'] = [0, 0, 50 * self.math.const['au']]
        new_command_line += self.get_command_line()
        self.parameter['position'] = [0, 0, -50 * self.math.const['au']]
        new_command_line += self.get_command_line()
        self.parameter['position'] = [0, 0, 60 * self.math.const['au']]
        new_command_line += self.get_command_line()
        self.parameter['position'] = [0, 0, -60 * self.math.const['au']]
        new_command_line += self.get_command_line()
        return new_command_line