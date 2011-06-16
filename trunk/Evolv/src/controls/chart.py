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
        cls.fp.write(", ".join(["type", "generation", "time"] + Phenotype.VALID) + "\n")

    @classmethod
    def append(cls, type, timestamp, generation, phenotype):
        if cls.fp is None:
            cls.clear()

        values = [type, str(generation), str(timestamp)]
        for name in Phenotype.VALID:
            phene = phenotype.get_phene(name)
            values.append(str(phene.get_value()))
        cls.fp.write(", ".join(values) + "\n")

class LiveLog(object):

    fp = None

    BIRTH = "b"
    AGE = "a"
    EATEN = "e"
    STARV = "s"

    @classmethod
    def clear(cls):
        cls.fp = open("live.log", "w")
        cls.fp.truncate(0)
        cls.fp.write(", ".join(["type", "time", "generation", "livetime", "event"]) + "\n")

    @classmethod
    def append(cls, type, timestamp, generation, livetime, event):
        if cls.fp is None:
            cls.clear()

        values = [type, str(timestamp), str(generation), str(livetime), event]
        cls.fp.write(", ".join(values) + "\n")
