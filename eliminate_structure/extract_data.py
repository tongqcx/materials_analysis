'''
The aim of this script is to eliminate the structures 
that have same space group and same formula, 
but different energy. The structure with lowest energy 
will be stroed in class Coms, other higher energy structure
will be discarded.

2019.09.10 tqc

'''
import os, sys
f = open('component_info.dat','r')
line = []
class Coms():
    def __init__(self):
        self.formula = {}
        self.na = {}
        self.sp = {}
        self.energy = {}
        self.record = []

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
            f.write('%20s %10d %10d %15.10f %20s\n' % (self.formula[iu], self.na[iu], self.sp[iu], self.energy[iu], iu))
        f.close()
coms = Coms()
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
