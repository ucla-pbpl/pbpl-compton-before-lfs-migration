#!/usr/bin/env python
import Geant4 as g4
from Geant4.hepunit import *
import numpy as np

def gamma_spray(energy=1*MeV, y0=0*mm):
    while 1:
        yield 'gamma', g4.G4ThreeVector(0, y0,-25*mm), g4.G4ThreeVector(0,0,1), energy
