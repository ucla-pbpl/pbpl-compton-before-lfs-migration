#!/usr/bin/env python
import sys
import toml
from pbpl import compton
import copy

def reconf(conf, material, num_events):
    result = copy.deepcopy(conf)
    result['Geometry']['World']['Material'] = material
    result['Detectors']['ComptonScintillator']['File'] = material + '.h5'
    result['PrimaryGenerator']['NumEvents'] = num_events
    return result

def main():
    tr = compton.TaskRunner()
    conf = toml.load('gas.toml')
    tr.add_task(compton.Task(reconf(conf, 'G4_Galactic', 1000000), 'vacuum'))
    tr.add_task(compton.Task(reconf(conf, 'G4_AIR', 1000000), 'air'))
    tr.add_task(compton.Task(reconf(conf, 'G4_He', 1000000), 'helium'))
    tr.add_task(compton.Task(reconf(conf, 'G4_Xe', 1000000), 'xenon'))
    tr.run()


if __name__ == '__main__':
    sys.exit(main())
