#!/usr/bin/env python
import sys
import numpy as np
from units import *


def main():
    m0 = me
    rest_energy = m0*c_light**2
    # omega0 = -40.70*deg
    # omega0 = -45*deg
    # omega0 = -60*deg
    omega0 = 0.0
    B0 = 1*tesla
    entrance_offset = 0.0*mm
    Ry = np.array((
        (np.cos(omega0), 0, np.sin(omega0)),
        (0, 1, 0),
        (-np.sin(omega0), 0, np.cos(omega0))))
    # nx = np.array((1, 0, 0))
    # ny = np.array((0, 1, 0))
    # nz = np.array((0, 0, 1))
    # print(Ry)
    # print(np.dot(Ry, nx))
    # print(np.dot(Ry, ny))
    # print(np.dot(Ry, nz))
    # sys.exit()

    energies = (30*MeV) * 2**np.arange(7) / 64
    # print(energies/MeV)
    # sys.exit()

    # print(energies/MeV)
    # sys.exit()
    f = open('Enge-C.pid', 'w')

    for kinetic_energy in energies:
        # for y0 in np.arange(-60*mm, 60*mm+0.01*mm, 10*mm):
        for y0 in [0,]:
            print(y0/mm)
            for q0 in [-eplus,]:
                # for theta in np.array((0,)):
                for theta in np.array((-2*deg, 0, 2*deg)):
                    # for phi in [90*deg]:
                    for phi in np.array((0,)):
                        # if phi == 90*deg:
                        #     continue
                        if phi == 90*deg and theta == 0:
                            continue
                        total_energy = rest_energy + kinetic_energy
                        gamma0 = total_energy/rest_energy
                        beta0 = np.sqrt(1-1/gamma0**2)
                        p0 = gamma0 * m0 * c_light * beta0
                        R0 = p0 / (abs(q0)*B0)
                        n0 = np.array(
                            (np.cos(phi)*np.sin(theta),
                             np.sin(phi)*np.sin(theta), np.cos(theta)))
                        x0 = np.array((entrance_offset, y0, 0))
                        beta0_gamma0 = np.dot(Ry, n0) * beta0 * gamma0
                        current = 1e-15*amp
                        f.write(
                            '{:12.5e} {:12.5e} {:12.5e} {:12.5e} {:12.5e} {:12.5e} {:12.5e} {:12.5e} {:12.5e}\n'.format(
                                *x0/meter, *beta0_gamma0, m0/kg, q0/coulomb, current/amp))

    f.close()

                    
if __name__ == '__main__':
    sys.exit(main())
