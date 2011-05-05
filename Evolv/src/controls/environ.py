'''
Created on 2011-05-05

@author: quermit
'''
import breve
from breve import Control

from simulation import player


class Environ(Control):

    def __init__(self):
        super(Environ, self).__init__()

        self.enableShadows()
        self.enableSmoothDrawing()
        self.enableLighting()
        self.moveLight(breve.vector(0, 20, 20))

        self.offsetCamera(breve.vector(0, 20, 0))
        self.aimCamera(breve.vector(0, 0, 0))

        player.play('hello')

    def iterate(self):
        super(Environ, self).iterate()
