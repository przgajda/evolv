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


class Environ(Control):
    
    Y = 0.0
    SIZE = 25.0

    def __init__(self):
        super(Environ, self).__init__()

        self.enableShadows()
        self.enableSmoothDrawing()
        self.enableLighting()
        self.moveLight(breve.vector(0, 100, 100))

        self.offsetCamera(breve.vector(0, 40, 0))
        self.aimCamera(breve.vector(0, 0, 0))

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
        
        wolfs = breve.createInstances(Wolf, 10)
        for wolf in wolfs:
            wolf.initWith(create_wolf_genotype())
            wolf.move(self.get_birthplace(wolf.size))

    def iterate(self):
        self.updateNeighbors()
        super(Environ, self).iterate()
