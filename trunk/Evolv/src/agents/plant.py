'''
Created on 2011-05-05

@author: quermit
'''
import random

import breve
from breve import Stationary
from breve import Sphere


class Plant(Stationary):

    MAXENERGY = 50

    def __init__(self):
        super(Plant, self).__init__()

        self.size = 0
        self.energy = random.randint(Plant.MAXENERGY / 2, Plant.MAXENERGY)

    def initWith(self):
        self.size = 0.2

        shape = breve.createInstances(Sphere, 1).initWith(self.size)
        self.setShape(shape)
        self.setColor(breve.vector(0.1, 0.9, 0.1))

        return self

    def update_energy(self, energy_change):
        energy = min(max(self.energy + energy_change, 0), Plant.MAXENERGY)
        self.energy = energy


breve.Plant = Plant
