# -*- coding: utf-8 -*-
import os, sys, random
import argparse
import numpy as np
import toml
from .core import setup_plot
from .core import pbpl_blue_cmap
from pbpl import compton
import Geant4 as g4
from Geant4.hepunit import *
import h5py
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plot
import matplotlib as mpl
from matplotlib.backends.backend_pdf import PdfPages

def get_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Plot energy deposition density',
        epilog='''\
Example:

.. code-block:: sh

  pbpl-compton-plot-deposition plot-deposition.toml
''')
    parser.add_argument(
        'config_filename', metavar='conf-file',
        help='Configuration file')
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

def plot_deposition_2d(output, conf, edep, xbin, ybin, zbin):
    mpl.rc('figure.subplot', right=0.97, top=0.96, bottom=0.13, left=0.13)
    fig = plot.figure(figsize=(244.0/72, 170.0/72))
    ax = fig.add_subplot(1, 1, 1, aspect=1)

    gammas_per_shot = conf['Files']['GammasPerShot']
    edep = edep.sum(axis=2)
    image = ax.imshow(
        edep.T/(GeV/gammas_per_shot), cmap=pbpl_blue_cmap,
        extent=(xbin[0]/mm, xbin[-1]/mm, ybin[0]/mm, ybin[-1]/mm))

    cb = fig.colorbar(image)
    cb.set_label(
        'GeV deposited per ' + conf['Annotation']['ShotLabel'],
        rotation=270, labelpad=10)
    ax.set_xlim(0, 320)
    ax.set_ylim(-140, 140)

    zp = np.linspace(0, 320, 320) * mm
    z = 10.0 + np.cos(40.0*deg) * zp

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

    output.savefig(fig, transparent=False)

def main():
    args = get_args()
    conf = args.conf
    fin = h5py.File(conf['Files']['Input'], 'r')
    run_index = tuple(conf['Files']['RunIndex'])
    edep = fin['edep'][run_index]*eV
    xbin = fin['xbin'][:]*mm
    ybin = fin['ybin'][:]*mm
    zbin = fin['zbin'][:]*mm

    setup_plot()

    out_fname = conf['Files']['Output']
    os.makedirs(os.path.dirname(out_fname), exist_ok=True)
    output = PdfPages(out_fname)
    plot_deposition_2d(output, conf, edep, xbin, ybin, zbin)
    output.close()
    return 0

if __name__ == '__main__':
    sys.exit(main())
