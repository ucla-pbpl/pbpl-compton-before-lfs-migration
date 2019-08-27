import numpy as np
from Geant4.hepunit import *

energies = np.array((1, 2, 4, 8, 16, 30)) * MeV
materials = ['G4_Galactic', 'G4_AIR', 'G4_He', 'G4_Xe']
material_labels = ['vacuum', 'air', 'helium', 'xenon']
y0 = np.array((0,)) * mm
dLi = np.array((5,)) * mm
