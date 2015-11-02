""" Get a puppet up and running

See: rst2py ?
"""
from docutils.parsers import rst
from docutils.nodes import document
from docutils.utils import new_document
from docutils.frontend import OptionParser

import inspect

from cogapp import Cog

class Bootstrap:

    def __init__(self):

        self.settings = OptionParser(
            components=(rst.Parser,)
            ).get_default_values()

    def interpret(self, data):

        self.parser = rst.Parser()
        self.document = new_document('.', settings)

        self.parser.parse(data, document)

    def say(self, *args, **kwargs):
        """ Write a python cog file interpreting rst """
        for item in data:
            print(' ' * depth, item, type(item).name)

            for sub in item:
                if str(sub) != sub:
                    dump(sub, depth+1)
        

    def dump(self):

        for item in data:
            print(' ' * depth, item, type(item))

            for sub in item:
                if str(sub) != sub:
                    dump(sub, depth+1)



