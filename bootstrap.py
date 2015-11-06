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

        self.depth = 0
        self.doc = ""
        self.name = ""
        self.attributes = {}
        self.parameters = []
        self.state = []

    def interpret(self, data):

        self.parser = rst.Parser()
        self.document = new_document('.', self.settings)

        self.parser.parse(data, self.document)

    def say(self, *args, **kwargs):
        """ Write a python cog file to interpret rst """
        self.response = []
        self.imports = []
        self.dump(self.document)

        print('imports:', self.imports)
        print('response:', self.response)
        return '\n'.join(self.imports + self.response)

    def dump(self, data, depth=0):

        print()
        for item in data:
            print('--' * (depth+2), str(item)[:30], type(item))

            self.update_attributes(item)

            name = item_name(item).lower()

            method = getattr(self, name, self.unknown)

            print(name)
            self.response.append(self.log(item, depth))
            #self.response.append(method(item, depth))
            
            method(item, depth)
            
            for sub in item.children:
                print("SUB", sub)
                #print(dir(sub))
                if str(sub) != sub:
                    self.dump(sub, depth+1)

        if self.state:
            method = self.state.pop()
            getattr(self, method)(item, depth)

        return

    def walk(self):

        self.document.walkabout(self)

    def dispatch_visit(self, *args):

        print('--' * self.depth, "VISIT: ", args)
        self.depth += 1

    def dispatch_departure(self, *args):

        self.depth -= 1
        print('--' * self.depth, "DEPART:", args)

    def update_attributes(self, item):
        """ Not sure if this helps or not """
        attributes = getattr(item, 'attributes', {})
        #print(attributes)
        self.attributes.update(attributes)
        #print(self.attributes)

    def log(self, item, depth):

        return "# %s: content: %s depth: %d" % (
            item_name(item), item.astext(), depth)


    def unknown(self, item, depth):

        return "# unknown: %s content: %s depth: %d" % (
            item_name(item), item.astext(), depth)

    def section(self, item, depth):
        """ Method or class depending on depth """
        print('SECTION')
        if not self.state:
            self.state.append('_class')
            return

        # Call method for current state
        method = self.state.pop()
        print("calling method:", method)
        getattr(self, method)(item, depth)
            
        self.state.append('_method')

    def title(self, item, depth):

        self.name = item.astext()

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

    def term(self, item, depth):

        self.action = item.astext()

    def definition_list(self, item, depth):

        pass

    def _method(self, item, depth):

        self.parameter_string = ','.join(
            self.parameters + ['*args', '**kwargs'])
            
        template = """
        def %(name)s(self, %(parameter_string)s):

            return "%(result)s"
        """
        print("XXX Method: ", self.name)
        self.write(template, depth)

    def _class(self, item, depth):

        template = '''
        class %(name)s:
            """ %(doc)s """
        '''
        print("XXX Class: ", self.name)
        self.write(template, depth)

    def write(self, template, depth):

        msg = template % self.__dict__

        self.response += self.form(msg, depth)

    def form(self, msg, depth):

        lines = msg.split('\n')
        tab = 4
        pad = " " * tab
        
        return [(depth * pad) + line[2*tab:]
                for line in lines]


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
