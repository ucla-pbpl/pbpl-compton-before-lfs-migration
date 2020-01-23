#!/usr/bin/env python
import sys
import numpy as np
from pbpl.compton.units import *

def main():
    m0 = me
    rest_energy = m0*c_light**2
    x0 = 0*mm
    z0 = 0*mm

    energy_vals = np.logspace(np.log10(0.240), np.log10(14.0), 40)*MeV
    y0_vals = np.arange(0, 40.01, 1)*mm
    print(energy_vals/MeV)
    print(y0_vals/mm)

    f = open('map-particles.pid', 'w')
    for kinetic_energy in energy_vals:
        for y0 in y0_vals:
            for q0 in [-eplus]:
                for theta in [0.0]:
                    for phi in [0.0]:
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
