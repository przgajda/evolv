'''
Created on 2011-05-05

@author: quermit
'''

from breve import Stationary


class Plant(Stationary):

    def __init__(self):
        super(Plant, self).__init__()

        self.energy = 0
