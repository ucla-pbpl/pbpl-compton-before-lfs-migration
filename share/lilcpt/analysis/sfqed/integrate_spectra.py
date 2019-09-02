#!/usr/bin/env python
import numpy as np
import sys
import h5py
from pbpl.compton.units import *
from scipy.integrate import simps
from scipy.stats import rv_histogram
from scipy.interpolate import interp1d

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

    print('Emin = {} MeV'.format(photon_energy[0]/MeV))
    print('Emax = {} MeV'.format(photon_energy[-1]/MeV))

    # /SFQED/MPIK/LCFA_w3.0_xi5.7/
    #
    #  E (MeV)   density (10^6 photons/MeV)
    #  ======    =========================
    #  5         1.85
    #  30        0.5
    #  100       0.2
    #
    #  9.8 mJ, 134e6 photons
    #


    # /SFQED/MPIK/LCS+LCFA_w3.0_xi5.7/
    #
    #
    #  E (MeV)   density (10^3 photons/MeV)
    #  ======    =========================
    #  5         115
    #  30        108
    #  100       85
    #
    #  9.1 mJ, 66e6 photons
    #

    energy = simps(spectral_energy_density, photon_energy)
    num_photons = simps(spectral_photon_density, photon_energy)
    print('integrated spectral energy = {} mJ'.format(energy/mJ))
    print('integrated number photons = {}'.format(num_photons))

    # hmmmm.. maybe d2W should contain bin edges?
    photon_energy_bins = np.append(photon_energy, photon_energy[-1]+1*MeV)
    photon_energy_binwidth = (
        photon_energy_bins[1:] - photon_energy_bins[:-1])
    rv = rv_histogram((spectral_photon_density, photon_energy_bins))

    for i in range(100):
        print(rv.rvs()/MeV)
    # sampled_photon_energies = np.array([rv.rvs() for x in range(1000000)])
    # test_hist, test_edges = np.histogram(
    #     sampled_photon_energies, bins=10000,
    #     range=(0*MeV, 10*GeV))
    # test_centers = 0.5*(test_edges[0:-1] + test_edges[1:])
    # np.savetxt(
    #     'sampled_histogram.dat', np.array(
    #         (test_centers/MeV, 134*test_hist)).T)

calc_integrals('../../../spectra/d2W.h5', '/SFQED/MPIK/LCFA_w3.0_xi5.7/')
#calc_integrals('../../../spectra/d2W.h5', '/SFQED/MPIK/LCS+LCFA_w3.0_xi5.7/')
