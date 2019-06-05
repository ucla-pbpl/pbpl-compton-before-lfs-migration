# -*- coding: utf-8 -*-
import matplotlib as mpl

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
    mpl.rc('legend', fontsize=8.0)
    mpl.rc('legend', labelspacing=0.25)
    mpl.rc('legend', frameon=False)
    mpl.rc('path', simplify=False)
    mpl.rc('axes', unicode_minus=False, linewidth=0.8)
    mpl.rc('figure.subplot', right=0.97, top=0.97, bottom=0.14, left=0.13)
    mpl.rc('axes', prop_cycle=mpl.cycler(
        'color', ['#0083b8', '#e66400', '#95b31b', '#a2448f']))
    mpl.rc('figure', max_open_warning=False)
