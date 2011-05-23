'''
Created on 2011-05-05

@author: quermit
'''
import time
import random

import breve
from breve import Control

from agents.animal import Rabbit, Wolf
from agents.genetics import create_rabbit_genotype, create_wolf_genotype, Genotype
from agents.plant import Plant


class Environ(Control):

    Y = 0.0
    SIZE = 40.0

    instance = None

    def __init__(self):
        super(Environ, self).__init__()

        Environ.instance = self

        self.enableShadows()
        self.enableSmoothDrawing()
        self.enableLighting()
        self.moveLight(breve.vector(0, 100, 100))

        self.offsetCamera(breve.vector(0, 60, 0))
        self.aimCamera(breve.vector(0, 0, 0))

        self.plants = []
        self.rabbits = []
        self.wolves = []
        self.rabbit_genotypes = []
        self.wolf_genotypes = []

        self.next_plant_born = time.time()

    @staticmethod
    def get_birthplace(animal_size):
        x = random.random()*Environ.SIZE - (Environ.SIZE / 2)
        z = random.random()*Environ.SIZE - (Environ.SIZE / 2)

        return breve.vector(x, Environ.Y + animal_size, z)

    def build(self):
        floor = breve.createInstances(breve.Floor, 1)
        floor.catchShadows()

        rabbits = breve.createInstances(Rabbit, 20)
        for rabbit in rabbits:
            rabbit.initWith(create_rabbit_genotype())
            rabbit.move(self.get_birthplace(rabbit.size))
        self.rabbits.extend(rabbits)

        wolves = breve.createInstances(Wolf, 10)
        for wolf in wolves:
            wolf.initWith(create_wolf_genotype())
            wolf.move(self.get_birthplace(wolf.size))
        self.wolves.extend(wolves)

        plants = breve.createInstances(Plant, 30)
        for plant in plants:
            plant.initWith()
            plant.move(self.get_birthplace(plant.size))
        self.plants.extend(plants)

    def iterate(self):
        super(Environ, self).iterate()

        if self.next_plant_born < time.time():
            self.bord_plant()
            self.next_plant_born = time.time() + random.random()*5.0 + 2.0

        for plant in self.plants:
            if plant.energy < 0.01:
                print "Plant eaten"
                self.plants.remove(plant)
                breve.deleteInstance(plant)

        for rabbit in self.rabbits:
            if rabbit.health < 0.01 and rabbit.energy < 0.01:
                print "Rabbit eaten"
                self.rabbits.remove(rabbit)
                breve.deleteInstance(rabbit)

        for wolf in self.wolves:
            if wolf.health < 0.01:
                print "Wolf eaten"
                self.wolves.remove(wolf)
                breve.deleteInstance(wolf)

        self.updateNeighbors()

    def born_wolf(self, wolf1, wolf2):
        genotype = Genotype.npoint_crossover(3, wolf1.genotype, wolf2.genotype)
        genotype = Genotype.npoint_random_mutation(2, genotype)
        self.wolf_genotypes.append(genotype)

        wolf = breve.createInstances(Wolf, 1)
        wolf.generation = max(wolf1.generation, wolf2.generation) + 1
        wolf.initWith(genotype)
        wolf.move(wolf1.getLocation())
        self.wolves.append(wolf)

    def born_rabbit(self, rabbit1, rabbit2):
        g1 = rabbit1.genotype
        g2 = rabbit2.genotype

        genotype = Genotype.npoint_crossover(2, g1, g2)
        genotype = Genotype.npoint_random_mutation(2, genotype)
        self.rabbit_genotypes.append(genotype)

        rabbit = breve.createInstances(Rabbit, 1)
        rabbit.generation = max(rabbit1.generation, rabbit2.generation) + 1
        rabbit.initWith(genotype)
        rabbit.move(rabbit1.getLocation())
        self.rabbits.append(rabbit)

    def bord_plant(self):
        plant = breve.createInstances(Plant, 1)
        plant.initWith()
        plant.move(self.get_birthplace(plant.size))
        self.plants.append(plant)


