#!/usr/bin/env python
import sys
from tempfile import NamedTemporaryFile
import subprocess
import toml
import numpy as np
from pbpl import compton
from Geant4.hepunit import *
import common

def main():
    conf = {}

    conf['Output'] = {
        'Filename' : 'out/reduced-edep.h5',
        'Group' : '/'
    }

    conf['Transformation'] = {
        'Translation' : [-25.0, 0.0, -10.0],
        'Rotation' : [0.0, 50.0, 0.0]
    }

    conf['Input'] = {}
    for i0, material_label in enumerate(common.material_labels):
        conf['Input'][str(i0)] = {}
        for i1, energy in enumerate(common.energies):
            conf['Input'][str(i0)][str(i1)] = {}
            for i2, y0 in enumerate(common.y0):
                conf['Input'][str(i0)][str(i1)][str(i2)] = {}
                for i3, dLi in enumerate(common.dLi):
                    filename = 'out/{}-{:.1f}MeV-{}mm-{:.1f}mm.h5'.format(
                        material_label, round(energy/MeV, 1),
                        int(round(y0/mm)), round(dLi, 1))
                    conf['Input'][str(i0)][str(i1)][str(i2)][str(i3)] = (
                        filename)

    # Need to convert numpy arrays to python lists because current
    # release of toml (0.10) writes numpy arrays as lists of strings
    # instead of lists of floats.  Next release of toml will include
    # a numpy-friendly encoder.
    conf['Indices'] = [
        { 'Label' : 'gas', 'Vals' : common.material_labels },
        { 'Label' : 'gamma energy', 'Vals' : (common.energies/MeV).tolist(),
          'Unit' : 'MeV'},
        { 'Label' : 'y0', 'Vals': (common.y0/mm).tolist(), 'Unit': 'mm' },
        { 'Label' : 'dLi', 'Vals': (common.dLi/mm).tolist(), 'Unit': 'mm' },
        { 'Label': 'x', 'Unit': 'mm',
          'NumBins': 60, 'LowerEdge': 0.0, 'UpperEdge': 300.0 },
        { 'Label': 'y', 'Unit': 'mm',
          'NumBins': 40, 'LowerEdge': -100.0, 'UpperEdge': 100.0 },
        { 'Label': 'z', 'Unit': 'mm',
          'NumBins': 4, 'LowerEdge': -10.0, 'UpperEdge': 10.0 } ]

    with NamedTemporaryFile('w', delete=False) as fout:
        conf_filename = fout.name
        toml.dump(conf, fout)
        fout.close()
    proc = subprocess.call(['pbpl-compton-reduce-edep', conf_filename])

if __name__ == '__main__':
    sys.exit(main())
