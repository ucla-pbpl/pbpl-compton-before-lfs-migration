#!/usr/bin/env python
import sys
import copy
import toml
import numpy as np
from pbpl import compton
from Geant4.hepunit import *
import common

def reconf(conf, desc, material, num_events, energy, y0, dLi):
    result = copy.deepcopy(conf)
    result['Geometry']['World']['Material'] = material
    pZ = float(0.5*dLi/mm)
    result['Geometry']['World']['Converter']['pZ'] = pZ
    result['Geometry']['World']['Converter']['Translation'][2] = -pZ
    result['Detectors']['ComptonScintillator']['File'] = 'out/' + desc + '.h5'
    result['PrimaryGenerator']['NumEvents'] = num_events
    result['PrimaryGenerator']['PythonGeneratorArgs'] = [
        '{}*MeV'.format(energy/MeV), '{}*mm'.format(y0/mm)]
    return result

def main():
    num_events = 10000000

    tr = compton.ParallelTaskRunner()
    conf = toml.load('gas.toml')
    for energy in common.energies:
        for material, label in zip(common.materials, common.material_labels):
            for y0 in common.y0:
                for dLi in common.dLi:
                    desc = '{}-{:.1f}MeV-{}mm-{:.1f}mm'.format(
                        label, round(energy/MeV, 1),
                        int(round(y0/mm)), round(dLi/mm, 1))
                    tr.add_task(compton.Task(
                        reconf(
                            conf, desc, material, num_events, energy, y0, dLi),
                        desc, 'pbpl-compton-mc'))
    tr.run()

if __name__ == '__main__':
    sys.exit(main())
