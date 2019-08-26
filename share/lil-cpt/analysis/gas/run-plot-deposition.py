#!/usr/bin/env python
import sys
import toml
import copy
import numpy as np
import h5py
from pbpl import compton
from Geant4.hepunit import *

def reconf(conf, run_index, gas, energy, y0, dLi):
    result = copy.deepcopy(conf)
    desc = '{}-{:.1f}MeV-{}mm-{:.1f}mm'.format(
        gas, round(energy/MeV, 1), int(round(y0/mm)), round(dLi/mm, 1))
    in_filename = 'out/' + desc + '.h5'
    out_filename = 'figs/' + desc + '.pdf'
    in_filename = 'out/{}-{:.1f}MeV-{}mm-{:.1f}mm.h5'.format(
        gas, round(energy/MeV, 1), int(round(y0/mm)), round(dLi/mm, 1))
    result['Files']['Output'] = out_filename
    result['Files']['RunIndex'] = run_index
    result['Annotation']['Text'] = [
        gas.title(),
        '$E_\gamma$ = {:.1f} MeV'.format(round(energy/MeV, 1)),
        r'$\ y_0$ = ' + '{} mm'.format(int(round(y0/mm))),
        r'$d_{\rm Li}$ = ' + '{:.1f} mm'.format(round(dLi/mm, 1))]
    return result

def main():
    tr = compton.SerialTaskRunner()
    conf = toml.load('plot-deposition.toml')
    fin = h5py.File(conf['Files']['Input'], 'r')
    for i0, gas in enumerate(x.decode('utf-8') for x in fin['i0'][:]):
        for i1, energy in enumerate(fin['i1'][:]*MeV):
            for i2, y0 in enumerate(fin['i2'][:]*mm):
                for i3, dLi in enumerate(fin['i3'][:]*mm):
                    desc = '{}-{:.1f}MeV-{}mm-{:.1f}mm'.format(
                        gas, round(energy/MeV, 1), int(round(y0/mm)),
                        round(dLi/mm, 1))
                    tr.add_task(compton.Task(
                        reconf(conf, (i0, i1, i2, i3), gas, energy, y0, dLi),
                        desc, 'pbpl-compton-plot-deposition'))
    fin.close()
    tr.run()

if __name__ == '__main__':
    sys.exit(main())
