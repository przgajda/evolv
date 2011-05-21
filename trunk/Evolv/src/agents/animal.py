'''
Created on 2011-05-05

@author: quermit
'''
import time
import random

import breve
from breve import Mobile
from breve import Sphere

from agents.genetics import Phenotype, Gene
from agents.plant import Plant
from meeting import RabbitPlantMeeting, WolfRabbitMeeting, RabbitRabbitMeeting


class Animal(Mobile):

    NEIGHBORHOOD = 5
    MAXHEALTH = 100
    MAXENERGY = 100

    def __init__(self):
        super(Animal, self).__init__()
        #self.handleCollisions('Animal', 'meet_agent')

        self.last_iter = time.time()

        self.genotype = None
        self.phenotype = None

        self.size = 0
        self.energy = Animal.MAXENERGY
        self.health = Animal.MAXHEALTH
        self.born_time = time.time()

        #self.showNeighborLines()
        self.setNeighborhoodSize(Rabbit.NEIGHBORHOOD)

        self.handleCollisions('Plant', 'meet_plant')
        self.handleCollisions('Rabbit', 'meet_rabbit')
        self.handleCollisions('Wolf', 'meet_wolf')
        self.update_health(self.health)

    def initWith(self, genotype):
        self.genotype = genotype
        self.phenotype = Phenotype.from_genotype(genotype)

        size_value = self.genotype.get_gene('size').get_value()
        self.size = 0.2 + (size_value - Gene.MIN + 0.1) / (Gene.MAX * 10.0)

        shape = breve.createInstances(Sphere, 1).initWith(self.size)
        self.setShape(shape)

        return self

    def get_age(self):
        return time.time() - self.born_time

    def meet_plant(self, plant):
        pass

    def meet_rabbit(self, rabbit):
        pass

    def meet_wolf(self, rabbit):
        pass

    def iterate(self):
        super(Animal, self).iterate()

        self.time_diff = time.time() - self.last_iter
        self.last_iter = time.time()

        self.check_location()

        if self.energy < 20:
            self.update_health(-self.time_diff)
        if self.energy > 50:
            self.update_health(3.0 * self.time_diff)

    def check_location(self):
        from controls.environ import Environ

        loc = self.getLocation()
        x = loc[0]
        z = loc[2]

        if x > Environ.SIZE / 2.0:
            x = -Environ.SIZE / 2.0 + 1.0
        if x < -Environ.SIZE / 2.0:
            x = Environ.SIZE / 2.0 - 1.0

        if z > Environ.SIZE / 2.0:
            z = -Environ.SIZE / 2.0 + 1.0
        if z < -Environ.SIZE / 2.0:
            z = Environ.SIZE / 2.0 - 1.0

        loc[0] = x
        loc[2] = z
        self.move(loc)

    def process_neighbors(self):
        neighbors = self.getNeighbors()
        rabbits = []
        wolfs = []
        plants = []
        for agent in neighbors:
            if isinstance(agent, Rabbit):
                rabbits.append(agent)
            if isinstance(agent, Wolf):
                wolfs.append(agent)
            if isinstance(agent, Plant):
                plants.append(agent)
        return rabbits, wolfs, plants

    def random_velocity(self):
        x = random.random() - 0.5
        z = random.random() - 0.5
        return breve.vector(x, 0.0, z)

    def go(self, vector, speed):
        if vector is None:
            self.setVelocity(breve.vector(0, 0, 0))
            return

        vector[1] = 0.0

        length = breve.length(vector)
        if length < 0.01:
            self.setVelocity(vector * speed)
            return

        vector = vector / length
        self.setVelocity(vector * speed)

    def update_energy(self, energy_change):
        energy = min(max(self.energy + energy_change, 0), Animal.MAXENERGY)
        self.energy = energy
        self.update_label()

    def update_health(self, health_change):
        health = min(max(self.health + health_change, 0), Animal.MAXHEALTH)
        self.health = health
        self.update_label()

    def update_label(self):
        self.setLabel("h: %d | e: %d" % (self.health, self.energy))


class Rabbit(Animal):

    SPEED = 0.2

    def __init__(self):
        super(Rabbit, self).__init__()

        self.next_v_update = 0

        self.setColor(breve.vector(0.9, 0.9, 0.9))

    def see_plants(self, plants):
        if not plants:
            return None

        closest = None
        for plant in plants:
            to_plant = plant.getLocation() - self.getLocation()
            if closest is None or breve.length(closest) > breve.length(to_plant):
                closest = to_plant
        return closest

    def meet_plant(self, plant):
        RabbitPlantMeeting(self, plant)

    def see_rabbits(self, rabbits):
        if not rabbits:
            return None

        if self.energy < 80 or self.get_age() < 15.0:
            return None

        #TODO: wybrac 1 krolika, drugi krolik musi potwierdzic chec :P
        rabbit = random.choice(rabbits)
        to_rabbit = rabbit.getLocation() - self.getLocation()
        return to_rabbit

    def meet_rabbit(self, rabbit):
        RabbitRabbitMeeting(self, rabbit)

    def see_wolfs(self, wolfs):
        if not wolfs:
            return None

        sum = breve.vector(0.0, 0.0, 0.0)
        for wolf in wolfs:
            from_wolf = self.getLocation() - wolf.getLocation()
            sum = sum + from_wolf * 1.0 / (breve.length(from_wolf) + 1.0)
        avg = sum / len(wolfs)
        return avg / breve.length(avg)

    def iterate(self):
        super(Rabbit, self).iterate()

        if self.health < 0.01:
            self.go(None)
            return  # rabbit died

        if self.next_v_update < time.time():
            self.next_v_update = time.time() + random.random()*3.0 + 1.0
            self.go(self.random_velocity())

        self.update_energy(-2.0 * self.time_diff);
        rabbits, wolfs, plants = self.process_neighbors()
        go_eat = self.see_plants(plants)
        go_rabbit = self.see_rabbits(rabbits)
        run_away = self.see_wolfs(wolfs)

        if run_away:
            self.go(run_away)
        elif self.energy < 80 and go_eat:
            self.go(go_eat)
        elif go_rabbit:
            self.go(go_rabbit)

    def go(self, vector):
        super(Rabbit, self).go(vector, Rabbit.SPEED)


class Wolf(Animal):

    SPEED = 0.3

    def __init__(self):
        super(Wolf, self).__init__()

        self.next_v_update = 0

        self.setColor(breve.vector(0.2, 0.2, 0.2))

    def see_wolfs(self, wolfs):
        pass

    def meet_wolf(self, rabbit):
        pass

    def see_rabbits(self, rabbits):
        if not rabbits:
            return None

        closest = None
        for rabbit in rabbits:
            to_rabbit = rabbit.getLocation() - self.getLocation()
            if closest is None or breve.length(closest) > breve.length(to_rabbit):
                closest = to_rabbit
        return closest

    def meet_rabbit(self, rabbit):
        WolfRabbitMeeting(self, rabbit)

    def iterate(self):
        super(Wolf, self).iterate()

        if self.health < 0.01:
            self.go(None)
            return  # wolf died

        if self.next_v_update < time.time():
            self.next_v_update = time.time() + random.random()*3.0 + 1.0
            self.go(self.random_velocity())

        self.update_energy(-2.0 * self.time_diff);
        rabbits, wolfs, _ = self.process_neighbors()
        chase = self.see_rabbits(rabbits)
        self.see_wolfs(wolfs)

        if self.energy < 80 and chase:
            self.go(chase)

    def go(self, vector):
        super(Wolf, self).go(vector, Wolf.SPEED)


breve.Animal = Animal
breve.Rabbit = Rabbit
breve.Wolf = Wolf
