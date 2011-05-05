'''
Created on 2011-05-05

@author: quermit
'''


class EvolvError(Exception):

    def __init__(self, *args, **kwargs):
        super(EvolvError, self).__init__(*args, **kwargs)
