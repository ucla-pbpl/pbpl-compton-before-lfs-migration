# -*- coding: utf-8 -*-
import os, sys, random
import argparse
import numpy as np
import toml
from .core import setup_plot
from pbpl import compton
import Geant4 as g4
from Geant4.hepunit import *
import h5py
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plot
#from .fake_parula import test_cm
import matplotlib as mpl

my_cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
    'my_cmap', ['#ffffff', '#0083b8'])
    # 'my_cmap', ['#ffffff', '#52a9cc', '#e68030'])

def get_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Plot energy deposition density',
        epilog='''\
Example:

.. code-block:: sh

  compton-mc --output=foo.h5 deposition.toml
''')
    parser.add_argument(
        '--output', default='deposition.pdf', metavar='out-file',
        help='Output PDF file (default=deposition.pdf)')
    parser.add_argument(
        'config_filename', metavar='conf-file',
        help='Configuration file')
    parser.add_argument(
        'input_filename', metavar='in-file',
        help='HDF5 SimpleDepositionSD input file')
    return parser

def get_args():
    parser = get_parser()
    args = parser.parse_args()
    args.conf = toml.load(args.config_filename)
    return args

def transform(position, translation, euler):
    result = []
    for r in position:
        rp = g4.G4ThreeVector(*r) + translation
        rp.rotateZ(euler[0])
        rp.rotateY(euler[1])
        rp.rotateZ(euler[2])
        result.append([rp.getX(), rp.getY(), rp.getZ()])
    return np.array(result)

def main():

    args = get_args()
    conf = args.conf
    fin = h5py.File(args.input_filename, 'r')
    edep = fin['edep'][:]*keV
    position = fin['position'][:]*mm
    num_gammas = fin['edep'].attrs['num_events']

    translation = g4.G4ThreeVector(
        *np.array(conf['Projection']['Translation'])*mm)
    euler = np.array(conf['Projection']['Rotation'])*deg

    tpos = transform(position, translation, euler)

    setup_plot()
    mpl.rc('figure.subplot', right=0.97, top=0.96, bottom=0.13, left=0.13)

    fig = plot.figure(figsize=(244.0/72, 170.0/72))
    ax = fig.add_subplot(1, 1, 1, aspect=1)


#    num_gammas = 2e6
    normalization = 1e9/num_gammas

    hist, xedges, yedges, image = ax.hist2d(
        tpos.T[0]/mm, tpos.T[1]/mm,
        # bins=(75,60),
        bins=(64,48),
        range=( (0, 320), (-120, 120)),
        weights = (normalization*edep/GeV),
        cmin=1,
        # cmap=test_cm,
        cmap=my_cmap,
        vmin=0)
#        vmin=0, vmax=100)
        #        density=True,
        # cmap='viridis')
#        cmap=cmap)

        # vmin=1,
        # vmax=1e5,
        # norm=SymLogNorm(linthresh=1, linscale=1)) #, vmin=-10.0, vmax=10000.0))
        #        norm=LogNorm(vmin=10.0, vmax=10000.0))

    cb = fig.colorbar(image)
    cb.set_label('GeV deposited per 10$^9$ gammas', rotation=270, labelpad=10)
    ax.set_xlim(0, 320)
    ax.set_ylim(-140, 140)
    # ax.set_xlim(0, 70)
    # ax.set_xlim(0, 2)
    # ax.set_ylim(-1, 1)

    zp = np.linspace(0, 320, 320) * mm
    z = 10.0 + np.cos(40.0*deg) * zp
    # print(z/mm)
    mag_d0 = conf['MagnetProfile']['d0'] * mm
    mag_c1 = conf['MagnetProfile']['c1'] * mm
    profile_zp = 0.5 * mag_d0 / (z/mag_c1)

    ax.plot(zp/mm, profile_zp/mm, color='k', linewidth=0.4)
    ax.plot(zp/mm, -profile_zp/mm, color='k', linewidth=0.4)

    text = ''
    for s in conf['Annotation']['Text']:
        text += '\n' + s
    ax.text(*conf['Annotation']['loc'], text, transform=ax.transAxes)

    ax.xaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator())
    ax.yaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator())

    ax.set_xlabel(r"$z'$ (mm)", labelpad=0.0)
    ax.set_ylabel(r'$y$ (mm)', labelpad=0.0)

    fig.savefig(args.output, transparent=False)

    return 0

if __name__ == '__main__':
    sys.exit(main())
