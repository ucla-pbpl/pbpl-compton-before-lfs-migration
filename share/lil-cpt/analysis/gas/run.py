#!/usr/bin/env python
import sys
import toml
import copy
import numpy as np
from pbpl import compton
from Geant4.hepunit import *

def reconf(conf, desc, material, num_events, energy, y0):
    result = copy.deepcopy(conf)
    result['Geometry']['World']['Material'] = material
    result['Detectors']['ComptonScintillator']['File'] = 'out/' + desc + '.h5'
    result['PrimaryGenerator']['NumEvents'] = num_events
    result['PrimaryGenerator']['PythonGeneratorArgs'] = [
        '{}*MeV'.format(energy/MeV), '{}*mm'.format(y0/mm)]
    return result

def main():
    num_events = 50000
    y0 = 0

    tr = compton.TaskRunner()
    conf = toml.load('gas.toml')
    for energy in np.array((1, 2, 4, 8, 16, 30)) * MeV:
        for material, name in zip(
                ['G4_Galactic', 'G4_AIR', 'G4_He', 'G4_Xe'],
                ['vacuum', 'air', 'helium', 'xenon']):
            desc = '{}-{}MeV-{}mm'.format(
                name, round(energy/MeV), round(y0/mm))
            tr.add_task(compton.Task(reconf(
                conf, desc, material, num_events, energy, y0), desc))
    tr.run()


if __name__ == '__main__':
    sys.exit(main())
