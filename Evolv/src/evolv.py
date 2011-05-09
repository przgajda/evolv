'''
Created on 2011-05-05

@author: quermit
'''
import time
import random

from controls.environ import Environ


def main():
    random.seed(time.time())
    
    global environment
    environment = Environ()
    environment.build()


if __name__ == '__main__':
    main()
