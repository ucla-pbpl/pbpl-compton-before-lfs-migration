#!/usr/bin/env python
import Geant4 as g4
from Geant4.hepunit import *
import numpy as np

# energies = (30.0 * MeV) * 2**np.arange(6)/32
# print(energies/MeV)
# [ 0.9375  1.875   3.75    7.5    15.     30.    ]

def electron_spray():
    energies = (30.0 * MeV) * 2**np.arange(6)/32
    for energy in energies:
        yield 'e-', g4.G4ThreeVector(), g4.G4ThreeVector(0,0,1), energy

def gamma_spray():
    energy = 1*MeV
    y0 = 0*mm
    while 1:
        yield 'gamma', g4.G4ThreeVector(0, y0,-25*mm), g4.G4ThreeVector(0,0,1), energy
