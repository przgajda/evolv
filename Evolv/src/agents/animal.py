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


class Animal(Mobile):

    NEIGHBORHOOD = 5
    MAXHEALTH = 100
    MOVE = -0.1

    def __init__(self):
        super(Animal, self).__init__()
        #self.handleCollisions('Animal', 'meet_agent')

        self.last_iter = 0

        self.genotype = None
        self.phenotype = None

        self.size = 0
        self.energy = 100
        self.health = Animal.MAXHEALTH
        self.age = 0

        self.showNeighborLines()
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

    def meet_plant(self, plant):
        pass

    def meet_rabbit(self, rabbit):
        pass

    def meet_wolf(self, rabbit):
        pass

    def iterate(self):
        self.last_iter = time.time()

        self.check_location()

        super(Animal, self).iterate()

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

    #def meet_agent(self, agent):
    #    if isinstance(agent, Rabbit):
    #        self.meet_rabit(agent)
    #    if isinstance(agent, Wolf):
    #        self.meet_wolf(agent)
    #    if isinstance(agent, Plant):
    #        self.meet_plant(agent)

    def random_velocity(self):
        x = random.random() - 0.5
        z = random.random() - 0.5
        return breve.vector(x, 0.0, z)

    def go(self, vector):
        vector = vector / breve.length(vector)
        vector[1] = 0.0
        self.setVelocity(vector / 5.0)

    def update_energy(self, energy_change):
        energy = max(self.energy + energy_change, 0)
        self.energy = energy
        if self.energy < 20 and energy_change < 0:
            self.update_health(self.health - max((20 - self.energy) * self.health / 20, 0.5))
        elif self.health < Animal.MAXHEALTH and energy_change > 0:
            self.update_health(self.health + energy_change / 2)

    def update_health(self, health):
        health = min(max(health, 0), Animal.MAXHEALTH)
        self.health = health
        print health
        self.setLabel(str(int(self.health)))

class Rabbit(Animal):

    def __init__(self):
        super(Rabbit, self).__init__()

        self.last_v_update = 0

        self.setColor(breve.vector(0.9, 0.9, 0.9))

    def see_plants(self, plants):
        if not plants:
            return None

        closest = None
        for plant in plants:
            to_plant = plant.getLocation() - self.getLocation()
            if closest is None or breve.length(closest) > breve.length(to_plant):
                closest = to_plant
        return closest / breve.length(closest)

    def meet_plant(self, plant):
        self.update_energy(plant.energy)
        plant.energy = 0

    def see_rabbits(self, rabbits):
        pass

    def meet_rabbit(self, rabbit):
        pass

    def see_wolfs(self, wolfs):
        if not wolfs:
            return None

        sum = breve.vector(0.0, 0.0, 0.0)
        for wolf in wolfs:
            from_wolf = self.getLocation() - wolf.getLocation()
            sum = sum + from_wolf * 1.0 / (breve.length(from_wolf) + 1.0)
        avg = sum / len(wolfs)
        return avg / breve.length(avg)

    def meet_wolf(self, wolf):
        energy_change = min(wolf.energy * 0.6, self.energy)
        if self.energy > 0:
            change_ratio = energy_change / self.energy
        else:
            change_ratio = 0
        self.update_health(self.health * (1 - change_ratio))
        self.update_energy(-energy_change)
        wolf.update_energy(energy_change)

    def iterate(self):
        if time.time() - self.last_v_update > 1.5:
            self.last_v_update = time.time()
            self.go(self.random_velocity())

        self.update_energy(Animal.MOVE);
        rabbits, wolfs, plants = self.process_neighbors()
        go_eat = self.see_plants(plants)
        self.see_rabbits(rabbits)
        run_away = self.see_wolfs(wolfs)

        if run_away:
            self.go(run_away)
        elif go_eat:
            self.go(go_eat)

        super(Rabbit, self).iterate()


class Wolf(Animal):

    def __init__(self):
        super(Wolf, self).__init__()

        self.last_v_update = 0

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
        return closest / breve.length(closest)

    def meet_rabbit(self, rabbit):
        energy_change = min(self.energy * 0.6, rabbit.energy)
        if rabbit.energy > 0:
            change_ratio = energy_change / rabbit.energy
        else:
            change_ratio = 0
        rabbit.update_health(rabbit.health * (1 - change_ratio))
        rabbit.update_energy(-energy_change)
        self.update_energy(energy_change)

    def iterate(self):
        if time.time() - self.last_v_update > 1.5:
            self.last_v_update = time.time()
            self.go(self.random_velocity())

        self.update_energy(Animal.MOVE);
        rabbits, wolfs, _ = self.process_neighbors()
        chase = self.see_rabbits(rabbits)
        self.see_wolfs(wolfs)

        if chase:
            self.go(chase)

        super(Wolf, self).iterate()


breve.Animal = Animal
breve.Rabbit = Rabbit
breve.Wolf = Wolf
