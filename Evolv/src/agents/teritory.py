'''
Created on 2011-06-01

@author: quermit
'''
import breve
from breve import Stationary
from breve import Cube


class Meadow(Stationary):

    def __init__(self):
        super(Meadow, self).__init__()

        print "New Meadow"

    def initWith(self, size):
        shape = breve.createInstances(Cube, 1).initWith(breve.vector(size, 0.8, size))
        self.setShape(shape)
        self.setColor(breve.vector(0.7, 0.9, 0.7))

        return self


class Forest(Stationary):

    def __init__(self):
        super(Forest, self).__init__()

        print "New Forest"

    def initWith(self, size):
        shape = breve.createInstances(Cube, 1).initWith(breve.vector(size, 0.8, size))
        self.setShape(shape)
        self.setColor(breve.vector(0.1, 0.5, 0.1))

        return self


breve.Meadow = Meadow
breve.Forest = Forest
