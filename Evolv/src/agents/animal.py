'''
Created on 2011-05-05

@author: quermit
'''
from breve import Mobile


class Animal(Mobile):

    def __init__(self):
        super(Animal, self).__init__()

        self.energy = 0
        self.health = 0
        self.age = 0


class Rabbit(Animal):

    def __init__(self):
        super(Rabbit, self).__init__()


class Wolf(Animal):

    def __init__(self):
        super(Rabbit, self).__init__()
