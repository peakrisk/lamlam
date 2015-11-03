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

cog.out(boot.say())
#cog.out("hello world")
"""

COG_RUN = """
if __name__ == '__main__':


    from cogapp import Cog

    Cog().main(['cog', '-cr', __file__])
"""

def item_name(item):

    return item.__class__.__name__

class Bootstrap:

    def __init__(self):

        self.settings = OptionParser(
            components=(rst.Parser,)
            ).get_default_values()

        self.attributes = {}

    def interpret(self, data):

        self.parser = rst.Parser()
        self.document = new_document('.', self.settings)

        self.parser.parse(data, self.document)

    def say(self, *args, **kwargs):
        """ Write a python cog file to interpret rst """
        self.response = []
        self.dump(self.document)

        return '\n'.join(self.response)

    def dump(self, data, depth=0):

        for item in data:
            print(' ' * depth, item, type(item))

            self.update_attributes(item)

            name = item_name(item)

            method = getattr(self, name, self.unknown)

            print(name)
            self.response.append(method(item, depth))

            for sub in item:
                if not str(sub) in sub:
                    self.dump(sub, depth+1)

        return

    def update_attributes(self, item):

        attributes = getattr(item, 'attributes', {})
        print(attributes)
        self.attributes.update(attributes)
        print(self.attributes)

    def unknown(self, item, depth):

        return "# unknkown: %s depth: %d" % (item_name(item), depth)

    def section(self, item, depth):
        """ Top section is a class """

        self.name = item.attributes['ids'][0]
        return self._class(item, depth)

    def paragraph(self, item, depth):
        """ Top section is a class """
        
        method = item.astext()
        self.method = clean_method_name(method)
        return ""

    def block_quote(self, item, depth):
        """ Complete a function """

        result = item.astext()
        self.result = result
        
        return self._method(item, depth)

    def _method(self, item, depth):

        TEMPLATE = """
        def %(method)s(self):

            return "%(result)s"
        """
        msg = TEMPLATE % self.__dict__

        return self.form(msg, depth)

    def _class(self, item, depth):

        TEMPLATE = """
        class %(name)s:
            pass

        """
        msg = TEMPLATE % self.__dict__

        return self.form(msg, depth)

    def form(self, msg, depth):

        lines = msg.split('\n')
        tab = 4
        pad = " " * tab
        
        return '\n'.join([(depth * pad) + line[2*tab:]
                          for line in lines])


def clean_method_name(method):

    method = method.strip(':?').replace(' ', '_')

    return method
    

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
