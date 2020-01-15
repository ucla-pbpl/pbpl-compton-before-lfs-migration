# -*- coding: utf-8 -*-
import numpy as np
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap
from scipy.spatial.transform import Rotation

def setup_plot():
    mpl.rc('font', size=8.0, family='sans-serif')
    mpl.rc('mathtext', fontset='cm')
    mpl.rc('pdf', use14corefonts=True)
    mpl.rc('lines', linewidth=0.8)
    mpl.rc('xtick.major', size=4)
    mpl.rc('ytick.major', size=4)
    mpl.rc('xtick', direction='in', top=True)
    mpl.rc('xtick.minor', size=2)
    mpl.rc('ytick.minor', size=2)
    mpl.rc('ytick', direction='in', right=True)
    mpl.rc('legend', fontsize=7.0)
    mpl.rc('legend', labelspacing=0.25)
    mpl.rc('legend', frameon=False)
    mpl.rc('path', simplify=False)
    mpl.rc('axes', unicode_minus=False, linewidth=0.8)
    mpl.rc('figure.subplot', right=0.97, top=0.97, bottom=0.15, left=0.13)
    mpl.rc('axes', titlepad=-10)
    mpl.rc('axes', prop_cycle=mpl.cycler(
        'color', [
            '#0083b8', '#e66400', '#93a661', '#ebc944', '#da1884', '#7e48bd']))
    # girl scouts green is 0x00ae58
    mpl.rc('figure', max_open_warning=False)

def gen_cdict(red, green, blue, midpoint, frac):
    return {'red':   [[0.0,  1.0, 1.0],
                      [midpoint,  red, red],
                      [1.0,  red*frac, red*frac]],
            'green': [[0.0,  1.0, 1.0],
                      [midpoint, green, green],
                      [1.0,  green*frac, green*frac]],
            'blue':  [[0.0,  1.0, 1.0],
                      [midpoint,  blue, blue],
                      [1.0,  blue*frac, blue*frac]]}

pbpl_blue_cmap = LinearSegmentedColormap(
    'pbpl_blue_cmap', segmentdata=gen_cdict(0, 0.51, 0.72, 0.75, 0.3), N=256)

pbpl_orange_cmap = LinearSegmentedColormap(
    'pbpl_orange_cmap', segmentdata=gen_cdict(0.90, 0.39, 0, 0.75, 0.3), N=256)

def build_transformation(spec, length_unit=1.0, angle_unit=1.0):
    result = np.identity(4)
    for operation, value in zip(*spec):
        translation = np.zeros(3)
        rotation = np.identity(3)
        if operation == 'TranslateX':
            translation = np.array((value*length_unit, 0, 0))
        if operation == 'TranslateY':
            translation = np.array((0, value*length_unit, 0))
        if operation == 'TranslateZ':
            translation = np.array((0, 0, value*length_unit))
        if operation == 'RotateX':
            rotation = Rotation.from_euler('x', value*angle_unit).as_dcm()
        if operation == 'RotateY':
            rotation = Rotation.from_euler('y', value*angle_unit).as_dcm()
        if operation == 'RotateZ':
            rotation = Rotation.from_euler('z', value*angle_unit).as_dcm()
        M = np.identity(4)
        M[:3,:3] = rotation
        M[:3,3] = translation
        result = M @ result
    return result

def transform(M, x):
    return (M[:3,:3] @ x) + M[:3,3]
