import string
from functools import reduce
import re
import sys
import time
class Components(object):

    def __init__(self):
        self.energy = {}
        self.spacegroup = {}
        self.Na = {}
        self.Name = {}
        self.Cif_name = {}

    def get_energy(self, name):
        return self.energy[name]

    def get_spacegroup(self, name):
        return self.spacegroup[name]

    def add_component(self, name, add_energy, spacegroup, struc, cif_name):
        name, n_formula, Name, Na = self._get_natoms(struc)  
        print(name, n_formula, Name, Na)
        if name in self.energy:
            if add_energy < self.energy[name]:
                self.energy[name] = add_energy
                self.spacegroup[name] = spacegroup
                self.Na[name] = Na
                self.Name[name] = Name
                self.Cif_name[name] = cif_name
        else:
            self.energy[name] = add_energy
            self.spacegroup[name] = spacegroup
            self.Na[name] = Na
            self.Name[name] = Name
            self.Cif_name[name] = cif_name
            
            
    def print_info(self):
        f = open('component_info.dat', 'w')
        for iu in self.energy:
            f.write('%s  %15.10f %15.10f  %s  %s\n' % (iu, self.formation_energy[iu], self.energy[iu], self.spacegroup[iu], self.Cif_name[iu]))
        f.close()

    def get_formation_energy(self):
        self.formation_energy = {}
        for iu in self.energy:
            self.formation_energy[iu] = self.energy[iu] * self.Na[iu]
            for ju in self.Name[iu]:
#                print(iu)
#                print(self.Name[iu])
#                print(ju, ju[:-1])
                self.formation_energy[iu] -= self.Name[iu][ju] * self.energy[ju + '1']

        return self.formation_energy

    def _numbersss(self,numbers):
        """
        Find the greatest common divisor
        """
        if len(numbers) == 1:
            
            return int(numbers[0]) 
        else:            
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

    def _get_natoms(self, struct):
        """
        Args:
            name: the formula, for example Al2Mg2O6
        Return:
            name: the reduced formula  for example AlMgO3
            n_formula:                             2
            Name:                                  {Al:1, Mg:1, O:3}
            Na: the number of atoms                5
        """           
        line=struct.split('\n')[11]
        if '_chemical_formula_sum' in line :
            a=(line.split('   '))[1].strip()
            if a[0] == "'" :
                a=eval(a)
            b=a.split(' ')
            element1=[]
            numbers=[]
            for i1 in b:
                s=i1.rstrip(string.digits)
                num= (re.findall(r"\d+\.?\d*",i1))
                element1.append(s)
                num=" ".join(num)
                numbers.append(num)
            n=self._numbersss(numbers)
            reduce_for=[]
            total=0
            dic={}
            for i in range(len(b)):
                dic[element1[i]]=int(int(numbers[i])/int(n))         
                reduce_for.append(element1[i])
                red=(int(int(numbers[i])/n))
                red1=str(red)
                total+= red
                reduce_for.append(red1)
            reduce_for1=(" ".join(reduce_for)) 
            reduce_for1=reduce_for1.replace(' ','')                  
            return (reduce_for1,n,dic,total) 
