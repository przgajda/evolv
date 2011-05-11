'''
Created on 2011-05-05

@author: quermit
'''
import breve
from breve import Stationary
from breve import Sphere


class Plant(Stationary):

    def __init__(self):
        super(Plant, self).__init__()

        self.size = 0
        self.energy = 0

    def initWith(self):
        self.size = 0.2

        shape = breve.createInstances(Sphere, 1).initWith(self.size)
        self.setShape(shape)
        self.setColor(breve.vector(0.1, 0.9, 0.1))

        return self


breve.Plant = Plant
