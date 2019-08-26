import Geant4 as g4
from Geant4.hepunit import *
import numpy as np

def gamma_spray(energy, y0):
    z0 = -25*mm
    direction = g4.G4ThreeVector(0,0,1)
    while 1:
        yield 'gamma', g4.G4ThreeVector(0, y0, z0), direction, energy
