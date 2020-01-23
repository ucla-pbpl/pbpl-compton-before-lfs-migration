#!/usr/bin/env python
import sys
import numpy as np
from units import *

def main():
    m0 = me
    rest_energy = m0*c_light**2
    x0 = 0*mm
    z0 = 0*mm

    energies = (28*MeV)/2**np.arange(6)
    energies = np.append(energies, (8*GeV)/2**np.arange(7))

    f = open('particles.pid', 'w')
    for kinetic_energy in energies:
        for y0 in [0*mm]:
            for q0 in [-eplus, eplus]:
                for theta in np.array((-2*deg, 0, 2*deg)):
                    if kinetic_energy>35*MeV:
                        if theta != 0:
                            continue
                    for phi in [0*deg]:
                        total_energy = rest_energy + kinetic_energy
                        gamma0 = total_energy/rest_energy
                        beta0 = np.sqrt(1-1/gamma0**2)
                        p0 = gamma0*m0*c_light*beta0
                        n0 = np.array(
                            (np.cos(phi)*np.sin(theta),
                             np.sin(phi)*np.sin(theta), np.cos(theta)))
                        r0 = np.array((x0, y0, z0))
                        beta0_gamma0 = n0 * beta0 * gamma0
                        current = 1e-15*amp
                        fmt = (
                            '{:12.5e} {:12.5e} {:12.5e} ' +
                            '{:12.5e} {:12.5e} {:12.5e} ' +
                            '{:12.5e} {:12.5e} {:12.5e}\n')
                        f.write(
                            fmt.format(*r0/meter, *beta0_gamma0,
                                       m0/kg, q0/coulomb, current/amp))
    f.close()

if __name__ == '__main__':
    sys.exit(main())
