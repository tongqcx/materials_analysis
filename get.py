#-*- coding: UTF-8 -*-
from pymatgen import MPRester
from pymatgen.analysis.phase_diagram import PhaseDiagram, PDPlotter
import collections
import sys, os
import time

os.system('rm -rf structure; mkdir structure')

ChemicalSymbols = [ 'H',  'He', 'Li', 'Be','B',  'C',  'N',  'O',  'F',
                    'Ne', 'Na', 'Mg', 'Al', 'Si','P',  'S',  'Cl', 'Ar', 'K',
                    'Ca', 'Sc', 'Ti', 'V',  'Cr','Mn', 'Fe', 'Co', 'Ni', 'Cu',
                    'Zn', 'Ga', 'Ge', 'As', 'Se','Br', 'Kr', 'Rb', 'Sr', 'Y',
                    'Zr', 'Nb', 'Mo', 'Tc', 'Ru','Rh', 'Pd', 'Ag', 'Cd', 'In',
                    'Sn', 'Sb', 'Te', 'I',  'Xe','Cs', 'Ba', 'La', 'Ce', 'Pr',
                    'Nd', 'Pm', 'Sm', 'Eu', 'Gd','Tb', 'Dy', 'Ho', 'Er', 'Tm',
                    'Yb', 'Lu', 'Hf', 'Ta', 'W','Re', 'Os', 'Ir', 'Pt', 'Au',
                    'Hg', 'Tl', 'Pb', 'Bi', 'Po','At', 'Rn', 'Fr', 'Ra', 'Ac',
                    'Th', 'Pa', 'U',  'Np', 'Pu','Am', 'Cm', 'Bk', 'Cf', 'Es',
                    'Fm', 'Md', 'No', 'Lr']
M = ['Sc', 'Ti', 'V', 'Cr', 'Mn',
     'Zr', 'Nb', 'Mo', 
     'Hf', 'Ta', 'W']
A = ['Al', 'Si', 'P', 'S',
     'Ga', 'Ge', 'As',
     'Cd', 'In', 'Sn',
     'Ti', 'Pb']
X = ['H',
     'B', 'C', 'N', 'O', 'F',
     'Si', 'P', 'S', 'Cl',
     'Br']

def get_formula(x, y, z):
    formula = []
    for ix in x:
        for iy in y:
            for iz in z:
                formula.append([ix, iy, iz])
    return formula

#comps = get_formula(M, A, X)
comps=[['Mg', 'Al', 'O']]
f=open('in.txt','w')
fcsv=open('id_prop.csv','w')
mpr = MPRester("7UnVyVXyetJ5WK3r")

for comp in comps:
    print(comp)
    try:
        entries = mpr.get_entries_in_chemsys(comp)
    except:
        continue
    if len(entries) == 0:
        continue
#    pd = PhaseDiagram(entries)
#    data = collections.defaultdict(list)
    for e in entries:
        #print(e)
        #print(type(e))
        #print(e.energy)
        print(e.entry_id, e.composition, e.energy)
        continue
        sys.exit(0)
#        ehull = pd.get_e_above_hull(e)
#        if ehull < 0.00000001 :
        com = e.entry_id
        start_time = time.time()
        prop = mpr.query(criteria={"task_id": com}, properties=[\
        "formation_energy_per_atom", \
        "energy_per_atom", \
        "spacegroup", \
        "pretty_formula", \
        "cif"])
        end_time = time.time()
        run_time = end_time - start_time
        print('run_time', run_time)

        form_energy =  prop[0]['formation_energy_per_atom']
        energy =  prop[0]['energy_per_atom']
        sp =  prop[0]['spacegroup']['symbol']
        name =  prop[0]['pretty_formula']
        struct = prop[0]['cif']

        fcif = open('./structure/' + com + '_' + name + '.cif','w')
        fcif.write(struct)
        fcif.close()
        f.write('%s  ' % name)
        f.write('%15.10f       %s\n' % (energy, com))
        fcsv.write(com + '_' + name + ',  ' + str(energy) + '  ' + str(form_energy) + '  ' + str(sp) + '\n')
f.close()
fcsv.close()

