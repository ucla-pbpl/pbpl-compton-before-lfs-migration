#!/usr/bin/env python
import Geant4 as g4
from Geant4.hepunit import *
import numpy as np
import h5py

def spectra_spray(filename, groupname):
    pass

def pattern_spray():
    energies = (26*MeV)/2**np.arange(5)
    for particle in ['e+', 'e-']:
        for energy in energies:
            yield particle, g4.G4ThreeVector(), g4.G4ThreeVector(0,0,1), energy

def repetitive_spray(particle, energy, x0, y0, z0):
    direction = g4.G4ThreeVector(0,0,1)
    while 1:
        yield particle, g4.G4ThreeVector(x0, y0, z0), direction, energy