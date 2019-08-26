#!/bin/sh
rm -rf out figs
echo '### RUNNING GEANT4 (./run-gas.py) ###'
./run-gas.py
echo '\n### BINNING ENERGY DEPOSITION (./run-reduce-edep.py) ###'
./run-reduce-edep.py
echo '\n### PLOTTING ENERGY DEPOSITION (./run-plot-deposition.py) ###'
./run-plot-deposition.py
