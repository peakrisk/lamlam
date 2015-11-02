""" Get a puppet up and running

See: rst2py ?
"""
import os
from docutils.parsers import rst
from docutils.nodes import document
from docutils.utils import new_document
from docutils.frontend import OptionParser

COG = """
from bootstrap import Bootstrap

# parse rest document

boot = Bootstrap()

rest = open("%(infile)s").read()

boot.interpret(rest)

#cog.out(boot.say())
cog.out("hello world")
"""

COG_RUN = """
if __name__ == '__main__':


    from cogapp import Cog

    Cog().main(['cog', '-cr', __file__])
"""


class Bootstrap:

    def __init__(self):

        self.settings = OptionParser(
            components=(rst.Parser,)
            ).get_default_values()

    def interpret(self, data):

        self.parser = rst.Parser()
        self.document = new_document('.', self.settings)

        self.parser.parse(data, self.document)

    def say(self, *args, **kwargs):
        """ Write a python cog file to interpret rst """
        self.dump(self.document)

    def dump(self, data, depth=0):

        for item in data:
            print(' ' * depth, item, type(item))

            name = item.__class__.__name__

            method = getattr(self, name, self.unknown)

            method()

    def unknown(self, item):

        print('unknown')

    def section(self, item):

        pass
        


if __name__ == '__main__':

    import sys


    for infile in sys.argv[1:]:

        base = infile.lstrip('rest').rstrip("rst")
        folder, module = os.path.split(base)

        out_folder = 'code' + folder
        os.makedirs(out_folder, exist_ok=True)
        
        outname = 'code' + base + 'py'
        print(outname)
        with open(outname, 'w') as outfile:
            print('""" Bootstrap cogging """', file=outfile)
            print(file=outfile)
            print('"""[[[cog', file=outfile)
            print(COG % locals(), file=outfile)
            print(']]]"""', file=outfile)
            print('#[[[end]]]', file=outfile)

            print(COG_RUN, file=outfile)
