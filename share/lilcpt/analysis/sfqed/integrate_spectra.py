#!/usr/bin/env python
import numpy as np
import h5py
from pbpl.compton.units import *
from scipy.integrate import simps

def calc_integrals(filename, groupname):
    print('===')
    print(groupname)
    fin = h5py.File(filename, 'r')
    g = fin[groupname]
    photon_energy = g['energy'][:]*MeV
    thetax = g['thetax'][:]*mrad
    thetay = g['thetay'][:]*mrad
    d2W = g['d2W'][:]*joule/(mrad**2*MeV)
    fin.close()
    dthetax = thetax[1]-thetax[0]
    dthetay = thetay[1]-thetay[0]

    spectral_energy_density = d2W.sum(axis=(1,2))*dthetax*dthetay
    spectral_photon_density = spectral_energy_density/photon_energy

    energy = simps(spectral_energy_density, photon_energy)
    num_photons = simps(spectral_photon_density, photon_energy)

    print('Emin = {} MeV'.format(photon_energy[0]/MeV))
    print('Emax = {} MeV'.format(photon_energy[-1]/MeV))

    print('integrated spectral energy = {} mJ'.format(energy/mJ))
    print('integrated number photons = {}'.format(num_photons))

calc_integrals('../../../spectra/d2W.h5', '/SFQED/MPIK/LCFA_w3.0_xi5.7/')
calc_integrals('../../../spectra/d2W.h5', '/SFQED/MPIK/LCS+LCFA_w3.0_xi5.7/')
