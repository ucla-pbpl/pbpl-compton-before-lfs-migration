#!/usr/bin/env python
import Geant4 as g4
from Geant4.hepunit import *
from scipy.integrate import simps
from scipy.stats import rv_histogram
import numpy as np
import h5py

def spectra_axial_spray(particle, filename, groupname, fraction_of_shot):
    print(particle, filename, groupname, fraction_of_shot)
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

    photon_energy_bins = np.append(photon_energy, photon_energy[-1]+1*MeV)
    photon_energy_binwidth = (
        photon_energy_bins[1:] - photon_energy_bins[:-1])
    rv = rv_histogram((spectral_photon_density, photon_energy_bins))

    num_events = int(fraction_of_shot*num_photons)
    print('num_events=', num_events)
    for i in range(num_events):
        energy = rv.rvs()
        print(i, energy/MeV)
        yield particle, g4.G4ThreeVector(), g4.G4ThreeVector(0,0,1), energy
    print('yo')
    raise StopIteration


def pattern_spray():
    energies = (26*MeV)/2**np.arange(5)
    for particle in ['e+', 'e-']:
        for energy in energies:
            yield particle, g4.G4ThreeVector(), g4.G4ThreeVector(0,0,1), energy

def repetitive_spray(particle, energy, x0, y0, z0):
    direction = g4.G4ThreeVector(0,0,1)
    while 1:
        yield particle, g4.G4ThreeVector(x0, y0, z0), direction, energy
