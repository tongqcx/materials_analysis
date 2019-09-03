#-*- coding: UTF-8 -*-
from pymatgen import MPRester
from pymatgen.analysis.phase_diagram import PhaseDiagram, PDPlotter
import collections
import sys, os
import time
import string
import re
from functools import reduce
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
f1=open('name.txt','w')

def numbersss(numbers):
    if len(numbers) == 1:
        return 1

#    elif len(numbers) == 2 :
#        a = int(numbers[0])
#        b = int(numbers[1])
#        if a>b:
#            t = a
#            a = b
#            b = t
#        for n  in range(1,1+(a)):
#            if (a)%n==0 and (b)%n==0:
#                i = [n]
#                i.sort()
#        return i[-1]
#
    else:            #len(numbers) > 2:
        mx = int(reduce(lambda x ,y: max(x,y),numbers))
        while True:
            flag =True
            for number in numbers :
                number=int(number)
                if  (number) % int(mx) !=0 :
                    flag = False
                    break
            if flag ==True:
                return mx

            mx -= 1
            
            




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
#        print(e.entry_id, e.composition, e.energy)
  #      continue
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
        #print('run_time', run_time)

        form_energy =  prop[0]['formation_energy_per_atom']
        energy =  prop[0]['energy_per_atom']
        sp =  prop[0]['spacegroup']['symbol']
        name =  prop[0]['pretty_formula']
#        print(name)
        f1.write(name+'\n')
        struct = prop[0]['cif']


        line=(struct.split('\n')[11])
        #line=(ccc[11])
        if '_chemical_formula_sum' in line :
            a=line.split('   ')[1].strip()
            #a=a[1]
            #a=a.strip()
            if a[0] == "'" :
                a=eval(a)
            b=a.split(' ')
            print(b) # 每个元素及数量
            print('-------')
            element1=[]
            numbers=[]
            for i1 in b:
                s=i1.rstrip(string.digits)
                num= (re.findall(r"\d+\.?\d*",i1))
                element1.append(s)
                num=" ".join(num)
                numbers.append(num)
            n=numbersss(numbers)
            print(numbers)
            print(n)
            reduce_for=[]
            total=0
            dic={}
            for i in range(len(b)):
                dic[element1[i]]=(int(int(numbers[i])/int(n)))
                reduce_for.append(element1[i])
                red=(int(int(numbers[i])/int(n)))
                red1=str(red)
                total+= red
                reduce_for.append(red1)
            print(reduce_for)
            reduce_for1=(" ".join(reduce_for)) 
            print(reduce_for1)
            reduce_for1=reduce_for1.replace(' ','')                  #(" ".join(reduce_for1.split(' ')))
            print(reduce_for1,n,dic,total)
            print('####################')









        fcif = open('./structure/' + com + '_' + name + '.cif','w')
        fcif.write(struct)
        fcif.close()
       # a=open('./structure/' + com + '_' + name + '.cif','r')
       # print(a)
       # while True:
       #     line=a.readline()
       #     if '_chemical_formula_sum' in line :
       #         a=(line.split()[1:])
       #         b=[str(i) for i in a]
       #         c=''.join(b)
       #         f1.write(c+'\n')
        f.write('%s  ' % name)
        f.write('%15.10f       %s\n' % (energy, com))
        fcsv.write(com + '_' + name + ',  ' + str(energy) + '  ' + str(form_energy) + '  ' + str(sp) + '\n')
f.close()
fcsv.close()
f1.close()
