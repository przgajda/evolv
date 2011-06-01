'''
Created on 2011-05-05

@author: quermit
'''
import random

from simulation.error import EvolvError


class Gene(object):

    MIN = -7.0
    MAX = 7.0

    def __init__(self, name, value):
        super(Gene, self).__init__()

        if name not in Genotype.VALID:
            raise EvolvError("Invalid gene name")

        self.name = name
        self.__value = value
        self.impacts = {}

    def get_value(self):
        return self.__value

    def set_value(self, value):
        self.__value = min(max(value, Gene.MIN), Gene.MAX)

    def add_impact(self, name, add=0.0):
        u"""
        Adding gene impact on phene of given name
        """
        if name not in Phenotype.VALID:
            raise EvolvError("Invalid phene")
        self.impacts[name] = lambda x, gv: x + add * gv

        return self

    def modify_phenotype(self, phenotype):
        u"""
        Apply gene impact on given phenotype
        """
        for phene in phenotype:
            if phene.name in self.impacts:
                func = self.impacts[phene.name]
                new_value = func(phene.get_value(), self.__value)
                phene.set_value(new_value)

    def __str__(self):
        return "<Gene %s : %.3f>" % (self.name, self.__value)


class Phene(object):

    def __init__(self, name, value):
        super(Phene, self).__init__()

        if name not in Phenotype.VALID:
            raise EvolvError("Invalid phene name")

        self.name = name
        self.__value = value

    def get_value(self):
        return self.__value

    def set_value(self, value):
        self.__value = value

    def __str__(self):
        return "<Phene %s : %.3f>" % (self.name, self.__value)


class Genotype(list):

    #VALID = """size ears legs tail teeth fur eyes pregnancy 
    #            stomach muzzle""".split()
    VALID = """size ears legs fur eyes""".split()

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

    @staticmethod
    def npoint_random_mutation(n, genotype):
        res = Genotype()
        res.extend(genotype[:])

        for _ in range(n):
            idx = random.randint(0, len(genotype) - 1)
            change = (random.random() - 0.5) * 1.0
            res[idx].set_value(res[idx].get_value() + change)

        return res

    def get_gene(self, name):
        for gene in self:
            if gene.name == name:
                return gene
        return None

    def __str__(self):
        out = []
        for gene in self:
            out.append(str(gene))
        return "Genotype: " + ", ".join(out)


class Phenotype(list):

#    VALID = """speed agility observation camouflage urge 
#                digestion effectiveness strength""".split()
    VALID = """speed observation camouflage strength""".split()

    def __init__(self, *args):
        super(Phenotype, self).__init__(*args)

    @staticmethod
    def from_genotype(genotype, default=1.0):
        u"""
        Constructs phenotype from genotype
        """
        res = Phenotype()

        for name in Phenotype.VALID:
            res.append(Phene(name, default))

        for gene in genotype:
            gene.modify_phenotype(res)

        return res

    def get_phene(self, name):
        for phene in self:
            if phene.name == name:
                return phene
        return None

    def __str__(self):
        out = []
        for phene in self:
            out.append(str(phene))
        return "Phenotype: " + ", ".join(out)


def create_simple_genotype(default=0.0):
    """
    Genes: size ears legs fur eyes
    Phenes: speed observation camouflage strength
    """
    g = Genotype()
    g.append(Gene('size', default)
             .add_impact('speed', add= -0.1)
             .add_impact('camouflage', add= -0.2)
             .add_impact('strength', add= +0.3))
    g.append(Gene('ears', default)
             .add_impact('speed', add= -0.2)
             .add_impact('observation', add= +0.4)
             .add_impact('camouflage', add= -0.2))
    g.append(Gene('legs', default)
             .add_impact('speed', add= +0.3)
             .add_impact('observation', add= +0.2)
             .add_impact('camouflage', add= -0.2)
             .add_impact('strength', add= -0.3))
    g.append(Gene('fur', default)
             .add_impact('speed', add= -0.3)
             .add_impact('camouflage', add= +0.3))
    g.append(Gene('eyes', default)
             .add_impact('observation', add= +0.4)
             .add_impact('camouflage', add= -0.1)
             .add_impact('strength', add= -0.3))
    return g


def create_rabbit_genotype():
    g = create_simple_genotype()
    g.get_gene('size').set_value(-2.0 + randsalt())
    g.get_gene('ears').set_value(4.0 + randsalt())
    g.get_gene('legs').set_value(1.0 + randsalt())
    g.get_gene('fur').set_value(3.0 + randsalt())
    g.get_gene('eyes').set_value(1.0 + randsalt())
    return g


def create_wolf_genotype():
    g = create_simple_genotype()
    g.get_gene('size').set_value(4.0 + randsalt())
    g.get_gene('ears').set_value(1.0 + randsalt())
    g.get_gene('legs').set_value(4.0 + randsalt())
    g.get_gene('fur').set_value(2.0 + randsalt())
    g.get_gene('eyes').set_value(1.0 + randsalt())
    return g

def randsalt():
    return random.random() - 0.5


if __name__ == '__main__':
    a = Genotype("abcde")
    b = Genotype("pqwxy")
    c = Genotype.npoint_crossover(2, a, b)
    print "%s (2-point crossover) %s => %s" % (a, b, c)

