'''
Created on 2011-05-05

@author: quermit
'''
import random

from simulation.error import EvolvError


class Gene(object):

    def __init__(self, name, value):
        super(Gene, self).__init__()

        if name not in Genotype.VALID:
            raise EvolvError("Invalid gene name")

        self.name = name
        self.value = value
        self.impacts = {}

    def append_impact(self, name, add, mul):
        u"""
        Append gene impact on phene of given name
        """
        if name not in Phenotype.VALID:
            raise EvolvError("Invalid phene")
        self.impacts[name] = lambda x: x * mul + add

    def modify_phenotype(self, phenotype):
        u"""
        Apply gene impact on given phenotype
        """
        for phene in phenotype:
            if phene.name in self.impacts:
                func = self.impacts[phene.name]
                new_value = func(phene.value)
                phene.value = new_value


class Phene(object):

    def __init__(self, name, value):
        super(Phene, self).__init__()

        if name not in Phenotype.VALID:
            raise EvolvError("Invalid phene name")

        self.name = name
        self.value = value


class Genotype(list):

    VALID = """size ears legs tail teeth fur eyes pregnancy 
                stomach muzzle""".split()

    def __init__(self, *args):
        super(Genotype, self).__init__(*args)

    @staticmethod
    def npoint_crossover(n, genotype_a, genotype_b):
        assert(len(genotype_a) == len(genotype_b))
        if n > len(genotype_a):
            raise EvolvError("N value is too large")

        res = Genotype()

        cuts = sorted(random.sample(range(len(genotype_a) + 1), n))
        last = 0
        for i, c in enumerate(cuts + [len(genotype_a)]):
            if i % 2 == 0:
                res.extend(genotype_a[last:c])
            else:
                res.extend(genotype_b[last:c])
            last = c
        return res


class Phenotype(list):

    VALID = """speed agility observation camouflage urge 
                digestion effectiveness""".split()

    def __init__(self, *args):
        super(Phenotype, self).__init__(*args)

    def from_genotype(self, genotype, default=0):
        u"""
        Constructs phenotype according to genotype
        """
        for name in Phenotype.VALID:
            self.append(Phene(name, default))

        for gene in genotype:
            gene.modify_phenotype(self)


if __name__ == '__main__':
    a = Genotype("abcde")
    b = Genotype("pqwxy")
    c = Genotype.npoint_crossover(2, a, b)
    print "%s (2-point crossover) %s => %s" % (a, b, c)

