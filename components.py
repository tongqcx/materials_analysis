import string
from functools import reduce
import re
class Components(object):

    def __init__(self):
        self.energy = {}
        self.spacegroup = {}
        self.Na = {}
        self.Name = {}

    def get_energy(self, name):
        return self.energy[name]

    def get_spacegroup(self, name):
        return self.spacegroup[name]

    def add_component(self, name, add_energy, spacegroup,struc):
        name, n_formula, Name, Na = self._get_natoms(struc)  
        print(name, n_formula, Name, Na)
        if name in self.energy:
            if add_energy < self.energy[name]:
                self.energy[name] = add_energy
                self.spacegroup[name] = spacegroup
                self.Na[name] = Na
                self.Name[name] = Name
        else:
            self.energy[name] = add_energy
            self.spacegroup[name] = spacegroup
            self.Na[name] = Na
            self.Name[name] = Name
            
            
    def print_info(self):
        f = open('component_info.dat', 'w')
        for iu in self.energy:
            f.write('%s  %15.10f  %s\n' % (iu, self.energy[iu], self.spacegroup[iu]))
        f.close()

    def get_formation_energy(self):
        self.formation_energy = {}
        for iu in self.energy:
            self.formation_energy[iu] = self.energy[iu] * self.Na[iu]
            for ju in self.Name:
                self.formation_energy[iu] -= self.Name[iu][ju] * self.energy[ju]
        return self.formation_energy

    def _numbersss(self,numbers):
        """
        Find the greatest common divisor
        """
        if len(numbers) == 1:
            return 1
     
        elif len(numbers) == 2 :
            a = int(numbers[0])
            b = int(numbers[1])
            if a>b:
                t = a
                a = b
                b = t
            for n  in range(1,1+(a)):
                if (a)%n==0 and (b)%n==0:
                    i = [n]
                    i.sort()
            return i[-1]

     
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
        ccc=(struct.split('\n'))
        line=(ccc[11])
        if '_chemical_formula_sum' in line :
            a=(line.split('   '))
            a=a[1]
            a=a.strip()
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
                red=(int(int(numbers[i])/int(n)))
                red1=str(red)
                total+= red
                reduce_for.append(red1)
            reduce_for1=(" ".join(reduce_for)) 
            reduce_for1=reduce_for1.replace(' ','')                  #(
            return (reduce_for1,n,dic,total) 
