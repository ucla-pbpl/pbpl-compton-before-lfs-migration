#!/usr/bin/env python
import sys
import matplotlib
import matplotlib.pyplot as plot
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from scipy.integrate import ode
from pbpl import compton
from pbpl.compton.units import *
from scipy.spatial import KDTree
from numpy.linalg import norm

def calc_trajectory(delta_t, y0, m0, q0, B):
    def yprime(t, y):
        x = y[:3]
        p = y[3:]
        p2 = np.dot(p, p)
        energy = np.sqrt(m0**2*c_light**4 + p2*c_light**2)
        B_x = B(x)
        dx = p*c_light**2/energy
        dp = q0 * np.cross(dx, B_x)
        return np.concatenate((dx, dp))
    solver = ode(yprime)
    solver.set_integrator('dopri5', max_step=1e-4)
    solver.set_initial_value(y0)
    trajectory = []
    times = []
    curr_t = 0.0
    while 1:
        trajectory.append(solver.integrate(curr_t))
        times.append(curr_t)
        curr_t += delta_t
        if trajectory[-1][1] < -10*mm:
            break
    return np.array(trajectory).T, np.array(times)

def calc_trajectories(kinetic_energy, alpha, dx):
    m0 = me
    q0 = -eplus
    rest_energy = m0*c_light**2
    total_energy = rest_energy + kinetic_energy
    gamma0 = total_energy/rest_energy
    beta0 = np.sqrt(1-1/gamma0**2)
    p0 = gamma0 * m0 * c_light * beta0
    dt = dx / (c_light * beta0)
    y0 = np.zeros(6)
    n0 = np.array((-np.sin(alpha), np.cos(alpha), 0))
    y0[3:] = n0*p0
    G0 = 3.6*tesla/meter
    def B(X):
        x = X[0]
        y = X[1]
        return np.array((0, 0, -G0*y))
    traj, times = calc_trajectory(dt, y0, m0, q0, B)
    diff = np.roll(traj[2], -1) - traj[2]
    return traj

def plot_fig(output, alpha0, label):
    fig = plot.figure(figsize=(244.0/72, 135.0/72))
    ax = fig.add_subplot(1, 1, 1, aspect='equal')
    ax.set_xlim(-240, 380)
    ax.set_ylim(0, 340)

    energies = (30*MeV) * 2**np.arange(7) / 64
    for kinetic_energy in energies:
        for dalpha, linewidth, opacity in zip(
                np.array((-5*deg, 0, 5*deg)),
                [0.2, 0.4, 0.2], [0.5, 1.0, 0.5]):
            traj = calc_trajectories(kinetic_energy, alpha0+dalpha, 2.5*mm)
            ax.plot(
                traj[0]/mm, traj[1]/mm, linewidth=linewidth,
                color='#0083b8', alpha=opacity)

    x0 = calc_trajectories(energies[-1], alpha0-5*deg, 0.5*mm)[0:2].T
    N = len(x0)
    x0 = x0[N//4:N-N//4]

    x1 = calc_trajectories(energies[-1], alpha0+5*deg, 0.5*mm)[0:2].T
    N = len(x1)
    x1 = x1[N//4:N-N//4]

    tree = KDTree(x0)
    x1_scan = np.array([tree.query(q) for q in x1])
    i1 = np.argmin(x1_scan.T[0])
    dist, i0 = tree.query(x1[i1])

    x0_f = 1.05*x0[i0]
    line_length = norm(x0_f)
    x0_0 = 0.6*line_length * np.array((-np.sin(alpha0), np.cos(alpha0)))
    ax.plot(
        [0, x0_f[0]/mm], [0, x0_f[1]/mm], color='#888888', linewidth=0.4,
        zorder=-10)
    ax.text(
        x0_f[0]/mm, x0_f[1]/mm, r' $\alpha_f = {:.1f}^\circ$'.format(
            90-np.arctan(x0_f[1]/x0_f[0])/deg), fontsize=7,
        verticalalignment='center')
    ax.plot(
        [0, x0_0[0]/mm], [0, x0_0[1]/mm], color='#888888', linewidth=0.4,
        zorder=-10)
    alpha0_label = r' $\alpha_0 = {:.1f}^\circ$'.format(alpha0/deg)
    ax.text(
        x0_0[0]/mm, x0_0[1]/mm, alpha0_label, fontsize=7,
        verticalalignment='center', horizontalalignment='right')

    plot.xlabel(r'$x$ (mm)', labelpad=0.0)
    plot.ylabel(r'$z$ (mm)', labelpad=0.0)

    if label is None:
        label = ''
    ax.text(
        0.03, 0.96,
        r'$B_y = G_0 z$' + '\n' +
        r'$G_0 = 3.6\;{\rm T/m}$' + '\n' + label, fontsize=7,
        verticalalignment='top',
        transform=ax.transAxes)
    ax.xaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator())
    ax.yaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator())
    output.savefig(fig, transparent=True)

def main():
    compton.setup_plot()
    output = PdfPages('trajectory-diagram.pdf')
    for alpha0, label in zip(
            np.array((40.7,30.0, 20.0, 10.0, 0.0, -10.0))*deg,
            ['Enge', None, None, None, 'CPT', None]):
        plot_fig(output, alpha0, label)
    output.close()

if __name__ == '__main__':
    sys.exit(main())
