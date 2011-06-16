'''
Created on 2011-05-05

@author: quermit
'''
import time
import random

import breve
from breve import Control

from agents.animal import Rabbit, Wolf, Animal
from agents.genetics import create_rabbit_genotype, create_wolf_genotype, Genotype
from agents.plant import Plant
from agents.teritory import Meadow, Forest
from controls.chart import PhenotypeLog, LiveLog


class Environ(Control):

    MAX_WOLVES = 20
    MAX_RABBITS = 60


    Y = 0.0
    SIZE = 40.0

    instance = None

    def __init__(self):
        super(Environ, self).__init__()

        Environ.instance = self

        self.beginTime = time.time()

        self.enableShadows()
        self.enableSmoothDrawing()
        self.enableLighting()
        self.moveLight(breve.vector(0, 100, 100))

        self.offsetCamera(breve.vector(0, 60, 0))
        self.aimCamera(breve.vector(0, 0, 0))

        self.plants = []
        self.rabbits = []
        self.wolves = []
        self.teritories = []
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
            self.__on_new_rabit(rabbit)

        wolves = breve.createInstances(Wolf, 10)
        for wolf in wolves:
            wolf.initWith(create_wolf_genotype())
            wolf.move(self.get_birthplace(wolf.size))
            self.__on_new_wolf(wolf)

        plants = breve.createInstances(Plant, 30)
        for plant in plants:
            plant.initWith()
            plant.move(self.get_birthplace(plant.size))
            self.__on_new_plant(plant)

        meadow = breve.createInstances(Meadow, 1)
        meadow.initWith(10.0)
        meadow.move(breve.vector(15, -0.1, 15))
        self.teritories.append(meadow)

        meadow = breve.createInstances(Meadow, 1)
        meadow.initWith(10.0)
        meadow.move(breve.vector(-15, -0.1, -15))
        self.teritories.append(meadow)

#        meadow = breve.createInstances(Meadow, 1)
#        meadow.initWith(10.0)
#        meadow.move(breve.vector(self.SIZE / 2, -0.1, -self.SIZE / 2))
#        self.teritories.append(meadow)
#
#        meadow = breve.createInstances(Meadow, 1)
#        meadow.initWith(10.0)
#        meadow.move(breve.vector(-self.SIZE / 2, -0.1, self.SIZE / 2))
#        self.teritories.append(meadow)
#
        meadow = breve.createInstances(Meadow, 1)
        meadow.initWith(15.0)
        meadow.move(breve.vector(-10, -0.1, 10))
        self.teritories.append(meadow)

        forest = breve.createInstances(Forest, 1)
        forest.initWith(10.0)
        forest.move(breve.vector(6, -0.1, -14))
        self.teritories.append(forest)

        forest = breve.createInstances(Forest, 1)
        forest.initWith(10.0)
        forest.move(breve.vector(12, -0.1, -4))
        self.teritories.append(forest)


    def iterate(self):
        super(Environ, self).iterate()

        if self.next_plant_born < time.time():
            self.bord_plant()
            self.next_plant_born = time.time() + random.random()*2.0 + 1.0

        try:
            for plant in self.plants:
                if plant.energy < 0.01:
                    print "Plant eaten"
                    self.plants.remove(plant)
                    breve.deleteInstance(plant)

            for rabbit in self.rabbits:
                if rabbit.fat < 0.01:
                    print "Rabbit eaten"
                    self.__on_rabbit_die(rabbit, LiveLog.EATEN)
                    self.rabbits.remove(rabbit)
                    breve.deleteInstance(rabbit)
                elif rabbit.get_age() > rabbit.die_at_age:
                    print "Rabbit died"
                    self.__on_rabbit_die(rabbit, LiveLog.AGE)
                    self.rabbits.remove(rabbit)
                    breve.deleteInstance(rabbit)
                elif rabbit.dead and not rabbit.was_eaten:
                    if not rabbit.logged:
                        print "Rabbit starved"
                    self.__on_rabbit_die(rabbit, LiveLog.STARV)
                elif rabbit.dead:
                    self.__on_rabbit_die(rabbit, LiveLog.EATEN)

            for wolf in self.wolves:
                if wolf.health < 0.01:
                    print "Wolf eaten"
                    self.wolves.remove(wolf)
                    self.__on_wolf_die(wolf, LiveLog.STARV)
                    breve.deleteInstance(wolf)
                elif wolf.get_age() > wolf.die_at_age:
                    print "Wolf died"
                    self.wolves.remove(wolf)
                    self.__on_wolf_die(wolf, LiveLog.AGE)
                    breve.deleteInstance(wolf)
        except Exception, e:
            print "ERROR: %s" % e

        self.updateNeighbors()

    def born_wolf(self, wolf1, wolf2):
        print "wolves #: %d" % len(self.wolves)
        if len(self.wolves) >= Environ.MAX_WOLVES:
            return

        genotype = Genotype.npoint_crossover(3, wolf1.genotype, wolf2.genotype)
        genotype = Genotype.npoint_random_mutation(2, genotype)
        self.wolf_genotypes.append(genotype)

        wolf = breve.createInstances(Wolf, 1)
        wolf.generation = max(wolf1.generation, wolf2.generation) + 1
        wolf.initWith(genotype)
        wolf.move(wolf1.getLocation())

        self.__on_new_wolf(wolf)

    def born_rabbit(self, rabbit1, rabbit2):
        print "rabbits #: %d" % len(self.rabbits)
        if len(self.rabbits) >= Environ.MAX_RABBITS:
            return

        g1 = rabbit1.genotype
        g2 = rabbit2.genotype

        genotype = Genotype.npoint_crossover(2, g1, g2)
        genotype = Genotype.npoint_random_mutation(2, genotype)
        self.rabbit_genotypes.append(genotype)

        rabbit = breve.createInstances(Rabbit, 1)
        rabbit.generation = max(rabbit1.generation, rabbit2.generation) + 1
        rabbit.initWith(genotype)
        rabbit.move(rabbit1.getLocation())

        self.__on_new_rabit(rabbit)

    def bord_plant(self):
        plant = breve.createInstances(Plant, 1)
        plant.initWith()
        plant.move(self.get_birthplace(plant.size))

        self.__on_new_plant(plant)

    def __on_new_plant(self, plant):
        self.plants.append(plant)

    def __on_new_rabit(self, rabbit):
        self.rabbits.append(rabbit)
        timestamp = time.time() - self.beginTime
        PhenotypeLog.append('rabbit', timestamp, rabbit.generation, rabbit.phenotype)
        LiveLog.append('rabbit', timestamp, rabbit.generation, 0, LiveLog.BIRTH)

    def __on_new_wolf(self, wolf):
        self.wolves.append(wolf)
        timestamp = time.time() - self.beginTime
        PhenotypeLog.append('wolf', timestamp, wolf.generation, wolf.phenotype)
        LiveLog.append('wolf', timestamp, wolf.generation, 0, LiveLog.BIRTH)

    def __on_rabbit_die(self, rabbit, type):
        if rabbit.logged :
            return
        rabbit.logged = True
        timestamp = time.time() - self.beginTime
        livetime = time.time() - rabbit.born_time
        print "rabbit", type
        LiveLog.append('rabbit', timestamp, rabbit.generation, livetime, type)

    def __on_wolf_die(self, wolf, type):
        if wolf.logged :
            return
        wolf.logged = True
        timestamp = time.time() - self.beginTime
        livetime = time.time() - wolf.born_time
        print "wolf", type
        LiveLog.append('wolf', timestamp, wolf.generation, livetime, type)

