'''
Created on 2011-05-05

@author: quermit
'''
import random

import breve
from breve import Mobile
from breve import Sphere

from agents.genetics import Phenotype, Gene


class Animal(Mobile):
    
    NEIGHBORHOOD = 5

    def __init__(self):
        super(Animal, self).__init__()
        
        self.genotype = None
        self.phenotype = None

        self.size = 0
        self.energy = 0
        self.health = 0
        self.age = 0
        
        self.showNeighborLines()
        self.setNeighborhoodSize(Rabbit.NEIGHBORHOOD)
        
        self.handleCollisions('Rabbit', 'meet_rabbit')
        self.handleCollisions('Wolf', 'meet_wolf')
        
    def initWith(self, genotype):
        self.genotype = genotype
        self.phenotype = Phenotype.from_genotype(genotype)
        
        size_value = self.genotype.get_gene('size').get_value()
        self.size = 0.2 + (size_value - Gene.MIN + 0.1) / (Gene.MAX * 10.0)
        
        shape = breve.createInstances(Sphere, 1).initWith(self.size)
        self.setShape(shape)
        
        return self
    
    def iterate(self):
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
        for agent in neighbors:
            if isinstance(agent, Rabbit):
                rabbits.append(agent)
            if isinstance(agent, Wolf):
                wolfs.append(agent)
        return rabbits, wolfs
    
    def random_velocity(self):
        x = random.random() - 0.5
        z = random.random() - 0.5 
        return breve.vector(x, 0.0, z)
    
    def go(self, vector):
        vector[1] = 0.0
        self.setVelocity(vector / 10.0)


class Rabbit(Animal):

    def __init__(self):
        super(Rabbit, self).__init__()

        self.setColor(breve.vector(0.9, 0.9, 0.9))
        
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
        pass
    
    def iterate(self):        
        self.setVelocity(self.random_velocity())
        
        rabbits, wolfs = self.process_neighbors()
        self.see_rabbits(rabbits)
        run_away = self.see_wolfs(wolfs)
        
        if run_away:
            self.go(run_away)
        
        super(Rabbit, self).iterate()


class Wolf(Animal):

    def __init__(self):
        super(Wolf, self).__init__()
        
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
    
    def meet_rabbit(self, wolf):
        pass
    
    def iterate(self):
        self.setVelocity(self.random_velocity())
        
        rabbits, wolfs = self.process_neighbors()
        chase = self.see_rabbits(rabbits)
        self.see_wolfs(wolfs)
        
        if chase:
            self.go(chase)
        
        super(Wolf, self).iterate()


breve.Animal = Animal
breve.Rabbit = Rabbit
breve.Wolf = Wolf
