'''
Created on 2011-05-05

@author: quermit
'''

import os

import breve
from breve import Sound

from simulation import config


__cache = {}


def play(name):
    music_path = config.get().get('paths', 'music')
    music_file = config.get().get('music', name)
    path = os.path.join(music_path, music_file)
    if name not in __cache:
        __cache[name] = breve.createInstances(Sound, 1).load(path)
    __cache[name].play()
