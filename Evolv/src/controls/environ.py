'''
Created on 2011-05-05

@author: quermit
'''
import random

import breve
from breve import Control

from simulation import player
from agents.animal import Rabbit, Wolf
from agents.genetics import create_rabbit_genotype, create_wolf_genotype
from agents.plant import Plant


class Environ(Control):

    Y = 0.0
    SIZE = 25.0

    instance = None

    def __init__(self):
        super(Environ, self).__init__()

        Environ.instance = self

        self.enableShadows()
        self.enableSmoothDrawing()
        self.enableLighting()
        self.moveLight(breve.vector(0, 100, 100))

        self.offsetCamera(breve.vector(0, 40, 0))
        self.aimCamera(breve.vector(0, 0, 0))

        self.plants = []
        self.rabbits = []
        self.wolves = []

        player.play('hello')

    @staticmethod
    def get_birthplace(animal_size):
        x = random.random()*Environ.SIZE - (Environ.SIZE / 2)
        z = random.random()*Environ.SIZE - (Environ.SIZE / 2)

        return breve.vector(x, Environ.Y + animal_size, z)

    def build(self):
        floor = breve.createInstances(breve.Floor, 1)
        floor.catchShadows()

        rabbits = breve.createInstances(Rabbit, 10)
        for rabbit in rabbits:
            rabbit.initWith(create_rabbit_genotype())
            rabbit.move(self.get_birthplace(rabbit.size))
        self.rabbits.extend(rabbits)

        wolves = breve.createInstances(Wolf, 5)
        for wolf in wolves:
            wolf.initWith(create_wolf_genotype())
            wolf.move(self.get_birthplace(wolf.size))
        self.wolves.extend(wolves)

        plants = breve.createInstances(Plant, 15)
        for plant in plants:
            plant.initWith()
            plant.move(self.get_birthplace(plant.size))
        self.plants.extend(plants)

    def iterate(self):
        super(Environ, self).iterate()

        for plant in self.plants:
            if plant.energy < 0.01:
                print "plant eaten"
                self.plants.remove(plant)
                breve.deleteInstance(plant)

        for rabbit in self.rabbits:
            if rabbit.health < 0.01 and rabbit.energy < 0.01:
                print "rabbit eaten"
                self.rabbits.remove(rabbit)
                breve.deleteInstance(rabbit)

        for wolf in self.wolves:
            if wolf.health < 0.01 and wolf.energy < 0.01:
                print "wolf eaten"
                self.wolves.remove(wolf)
                breve.deleteInstance(wolf)

        self.updateNeighbors()

    def born_rabbit(self, rabbit1, rabbit2):
        print "rabbit borned"
        pos = rabbit1.getLocation()
        rabbit = breve.createInstances(Rabbit, 1)
        rabbit.initWith(create_rabbit_genotype())
        rabbit.move(pos)
        self.rabbits.append(rabbit)


