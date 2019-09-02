
class Components(object):

    def __init__(self):
        self.energy = {}
        self.spacegroup = {}

    def get_energy(self, name):
        return self.energy[name]

    def get_spacegroup(self, name):
        return self.spacegroup[name]

    def add_component(self, name, add_energy, spacegroup):
        if name in self.energy:
            if add_energy < self.energy[name]:
                self.energy[name] = add_energy
                self.spacegroup[name] = spacegroup
        else:
            self.energy[name] = add_energy
            self.spacegroup[name] = spacegroup
            
    def print_info(self):
        f = open('component_info.dat', 'w')
        for iu in self.energy:
            f.write('%s  %15.10f  %s\n' % (iu, self.energy[iu], self.spacegroup[iu]))
        f.close()
