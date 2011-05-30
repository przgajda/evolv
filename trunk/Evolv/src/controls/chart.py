'''
Created on 2011-05-30

@author: quermit
'''
from agents.genetics import Phenotype


class PhenotypeLog(object):

    fp = None

    @classmethod
    def clear(cls):
        cls.fp = open("genetics.log", "w")
        cls.fp.truncate(0)
        cls.fp.write(", ".join(["type", "generation"] + Phenotype.VALID) + "\n")

    @classmethod
    def append(cls, type, generation, phenotype):
        if cls.fp is None:
            cls.clear()

        values = [type, str(generation)]
        for name in Phenotype.VALID:
            phene = phenotype.get_phene(name)
            values.append(str(phene.get_value()))
        cls.fp.write(", ".join(values) + "\n")
