#!/usr/bin/env python
import os
import toml

os.system('rm -f *wrl *h5')

print('### RUNNING GEANT4 (LCFA, a0=5.7) ###')
conf = toml.load('lilcpt.toml')
A = conf['PrimaryGenerator']
A['PythonGenerator'] = 'lilcpt.spectra_axial_spray'
A['PythonGeneratorArgs'] = [
    'gamma', '../../../spectra/d2W.h5', '/SFQED/MPIK/LCFA_w3.0_xi5.7/',
    '0.0001']
A['NumEvents']= 1000000000
with open('temp.toml', 'w') as fout:
    toml.dump(conf, fout)
os.system('pbpl-compton-mc temp.toml')
#os.system('pbpl-compton-mc temp.toml > /dev/null 2>&1')
#os.system('rm -f temp.toml g4*wrl *h5')

# print('### RUNNING GEANT4 (gamma-20MeV.wrl) ###')
# conf = toml.load('lilcpt.toml')
# A = conf['PrimaryGenerator']
# A['PythonGenerator'] = 'lilcpt.repetitive_spray'
# A['PythonGeneratorArgs'] = ['gamma', '20*MeV', '0*mm', '0*mm', '-10*mm']
# A['NumEvents'] = 10000
# with open('temp.toml', 'w') as fout:
#     toml.dump(conf, fout)
# os.system('pbpl-compton-mc temp.toml > /dev/null 2>&1')
# os.system('pbpl-compton-extrude-vrml g4_00.wrl --radius=1.0 --num-points=8 --output=gamma-20MeV.wrl')
# os.system('rm -f temp.toml g4*wrl *h5')
