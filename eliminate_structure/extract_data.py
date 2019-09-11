'''
The aim of this script is to eliminate the structures 
that have same space group and same formula, 
but different energy. The structure with lowest energy 
will be stroed in class Coms, other higher energy structure
will be discarded.

2019.09.10 tqc

'''
import os, sys
class Coms():
    def __init__(self, lform_e):
        ChemicalSymbols = [ 'X',  'H',  'He', 'Li', 'Be','B',  'C',  'N',  'O',  'F',
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
        self.formula = {}
        self.na = {}
        self.sp = {}
        self.energy = {}
        self.record = []
        self.lform_e = lform_e
        if self.lform_e:
            self.element_energy = self._read_element_energy()
            self.formation_energy = {}
            self.atomicNum = {}
            for anum, symbol in enumerate(ChemicalSymbols):
                self.atomicNum[anum] = symbol


    def _read_element_energy(self):
        try:
            f = open('element_energy_mp.dat', 'r')
        except:
            print ' '
            sys.exit(0)
        line = []
        energy = {}
        while True:
            line = f.readline().split()
            if len(line) == 0:
                break
            coms = line[0][:-1]
            ene = float(line[2])
            energy[coms] = ene
        return energy

    def _get_dict_value(self, idict):
        ilist = []
        for i in idict:
            ilist.append(idict[i])
        return ilist

    #def _get_dict_key(self, idict):
    #    ilist = []
    #    for i in idict:
    #        ilist.append(i)
    #    return ilist

    def _get_dict_key(self, my_dict, my_value):
        my_list = []
        for iu in my_dict:
            if my_dict[iu] == my_value:
                my_list.append(iu)
        return my_list

    def _add_id(self, id, iformula, ina, isp, ienergy):
            self.formula[id] = iformula
            self.na[id] = ina
            self.sp[id] = isp
            self.energy[id] = ienergy
            self.record.append(id)

    def _delete_id(self, id):
            del self.formula[id]
            del self.na[id]
            del self.sp[id]
            del self.energy[id]
            self.record.remove(id)


    def add_element(self, iformula, ina, isp, ienergy, id):
        if iformula in self._get_dict_value(self.formula):
            key_id = self._get_dict_key(self.formula, iformula)
            for ikey_id in key_id:

                if isp == self.sp[ikey_id] and ienergy >= self.energy[ikey_id]:
                    return

                if isp == self.sp[ikey_id] and ienergy < self.energy[ikey_id]:
                    self._delete_id(ikey_id)
                    self._add_id(id, iformula, ina, isp, ienergy)
                    return
            self._add_id(id, iformula, ina, isp, ienergy)
            
        else:
            self._add_id(id, iformula, ina, isp, ienergy)

    def print_info(self):
        f = open('training.dat','w')
        for iu in self.record:
            if self.lform_e:
                form_e = self._get_form_energy(iu)
                f.write('%20s %10d %10d %15.10f %15.10f %20s\n' % (self.formula[iu], self.na[iu], self.sp[iu], form_e, self.energy[iu], iu))
            else:
                f.write('%20s %10d %10d %15.10f %20s\n' % (self.formula[iu], self.na[iu], self.sp[iu], self.energy[iu], iu))
        f.close()

    def get_formation_energy(self):
        for iu in self.record:
            self.formation_energy[iu] = self._get_form_energy(iu)

    def _get_form_energy(self, iu):
        coms = self.formula[iu]
        namelist, numlist = self._readComponent(coms)
        NA = sum(numlist)
        form_e = self.energy[iu] * NA
        for i in range(len(namelist)):
            print numlist[i], namelist[i], self.element_energy[namelist[i]]
            form_e -=  numlist[i] * self.element_energy[namelist[i]]
        return form_e/NA
            

    def _readComponent(self, comps):
        namelist = []
        numlist = []
        ccomps = comps
        while(len(ccomps) != 0):
            stemp = ccomps[1:]
            if(len(stemp) == 0):
                namelist.append(ccomps)
                numlist.append(1.0)
                break
            it = 0
            for st in stemp:
                it = it + 1
                if(st.isupper()):
                    im = 0
                    for mt in stemp[:it]:
                        im = im + 1
                        if(mt.isdigit()):
                            namelist.append(ccomps[0:im])
                            numlist.append(float(ccomps[im:it]))
                            ccomps = ccomps[it:]
                            break
                        elif(im == len(stemp[:it])):
                            namelist.append(ccomps[0:im])
                            numlist.append(1.0)
                            ccomps = ccomps[it:]
                            break
                    break
                elif(it == len(stemp)):
                    im = 0
                    for mt in stemp:
                        im = im + 1
                        if(mt.isdigit()):
                            namelist.append(ccomps[0:im])
                            numlist.append(float(ccomps[im:]))
                            ccomps = ccomps[it+1:]
                            break
                        elif(im == len(stemp)):
                            namelist.append(ccomps)
                            numlist.append(1.0)
                            ccomps = ccomps[it+1:]
                            break
                    break
        return namelist, numlist
    
        
#===============================================================================
#f = open('component_info.dat','r')
f = open('component_info.dat','r')
line = []
lform_e = True
coms = Coms(lform_e)
i = 0
while True:
    line = f.readline().split()
    if len(line) == 0:
        break
    try:
        formula = line[0]
        na = int(line[1])
        sp = int(line[2])
        energy = float(line[3])
        id = line[4]
    except:
        continue
    coms.add_element(formula, na, sp, energy, id)
coms.print_info()
