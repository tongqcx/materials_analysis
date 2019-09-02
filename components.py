
class Components(object):

    def __init__(self):
        self.energy = {}

    def get_energy(self, name):
        return min(self.energy[name])

    def add_component(self, name, add_energy):
        self.energy[name].append(add_energy)
