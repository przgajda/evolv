'''
Created on 2011-05-05

@author: quermit
'''
import ConfigParser


__config = ConfigParser.ConfigParser()
__config.read('evolv.cfg')


def get():
    return __config
