""" Just write this thing

See: rst2py
"""
import docutils

import inspect

from cogapp import Cog

class Bootstrap:

    def interpret(self, *args, **kwargs):

        infile = kwarg.get('infile')

        for item in infile:
            self.say(self.interpret(item))
    
    def say(self, *args, **kwargs):
        pass
    
