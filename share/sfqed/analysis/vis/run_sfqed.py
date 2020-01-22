#!/usr/bin/env python
import os
import toml

#os.system('rm -f *wrl *h5')

#print('### RUNNING GEANT4 (design.wrl) ###')
#conf = toml.load('sfqed-uncol.toml')
#A = conf['PrimaryGenerator']
#A['PythonGenerator'] = 'sfqed.pattern_spray'
#A['NumEvents']= 100
#with open('temp.toml', 'w') as fout:
#    toml.dump(conf, fout)
#os.system('pbpl-compton-mc temp.toml vis.mac')
#os.system('pbpl-compton-extrude-vrml g4_00.wrl --radius=1.0 --num-points=8 --output=design.wrl')
#os.system('rm -f temp.toml g4*wrl')

print('### RUNNING GEANT4 Collimanted (gamma-20MeV.wrl) ###')
conf = toml.load('sfqed.toml')
A = conf['PrimaryGenerator']
A['PythonGenerator'] = 'sfqed.pattern_spray'#repetitive_spray'
A['PythonGeneratorArgs'] = ['20000000']
A['NumEvents'] = 20000000
with open('temp.toml', 'w') as fout:
    toml.dump(conf, fout)
os.system('pbpl-compton-mc temp.toml vis.mac')
os.system('pbpl-compton-extrude-vrml g4_00.wrl --radius=1.0 --num-points=8 --output=gamma-20MeV.wrl')
#os.system('rm -f temp.toml g4*wrl')

#print('### RUNNING GEANT4 Uncollimanted (gamma-20MeV.wrl) ###')
#conf = toml.load('sfqed-uncol.toml')
#A = conf['PrimaryGenerator']
#A['PythonGenerator'] = 'sfqed.repetitive_spray'
#A['PythonGeneratorArgs'] = ['gamma', '20*MeV', '0*mm', '0*mm', '-10*mm']
#A['NumEvents'] = 10000000
#with open('temp.toml', 'w') as fout:
#    toml.dump(conf, fout)
#os.system('pbpl-compton-mc temp.toml vis.mac')
#os.system('pbpl-compton-extrude-vrml g4_00.wrl --radius=1.0 --num-points=8 --output=gamma-20MeV.wrl')
#os.system('rm -f temp.toml g4*wrl')