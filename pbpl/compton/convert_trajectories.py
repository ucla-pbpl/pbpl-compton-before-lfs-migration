#!/usr/bin/env python
import sys
import numpy as np
import ezdxf

meter = 1.0
mm = 1e-3*meter

def main():
    A = np.loadtxt(
        'trajectories.txt', usecols=(0,2,10), dtype=np.float, skiprows=7)
    dwg = ezdxf.new('R2000')
    msp = dwg.modelspace()
    for i in range(int(A[:,2].max())+1):
        mask = A[:,2] == i
        x = A[mask,0]*meter
        y = A[mask,1]*meter
        msp.add_lwpolyline(np.array((x/mm, y/mm)).T)
    dwg.saveas('trajectories.dxf')

if __name__ == '__main__':
    sys.exit(main())
