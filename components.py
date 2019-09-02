
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

    def add_component(self, name, add_energy, spacegroup):
        name, n_formula, Name, Na = self._get_natoms(name)  
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

    def _get_natoms(self, name):
        """
        Args:
            name: the formula, for example Al2Mg2O6
        Return:
            name: the reduced formula  for example AlMgO3
            n_formula:                             2
            Name:                                  {Al:2, Mg:2, O:6}
            Na: the number of atoms                10
        """   
