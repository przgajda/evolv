'''
Created on 2011-05-05

@author: quermit
'''

"""
genotype:
    size
    ears
    legs
    tail
    teeth
    fur
    eyes
    pregnancy
    stomach
    muzzle

fenotype:
    speed
    agility
    observation
    camouflage
    urge
    digestion
    effectiveness
"""

class Gene(object):

    def __init__(self, name, value):
        super(Gene, self).__init__()

        self.name = name
        self.value = value
        self.impacts = {}

    def append_impact(self, name, add, mul):
        self.impacts[name] = lambda x: x * mul + add

    def process_phene(self, name, value):
        func = self.impacts.get(name, lambda x: x)
        return func(value)


class Phene(object):

    def __init__(self, name, value):
        super(Phene, self).__init__()

        self.name = name
        self.value = value


class Genotype(object):

    def __init__(self):
        super(Genotype, self).__init__()


class Phenotype(object):
    def __init__(self):
        super(Phenotype, self).__init__()
