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

        item = args[0]
        name = item_name(item)
        method = getattr(self, 'visit_' + name, self.unknown)

        print(name)
        method(item)
        self.log(item)

        print('--' * self.depth, "VISIT: ", len(args), args, name)
        self.depth += 1

    def dispatch_departure(self, *args):

        self.depth -= 1
        print('--' * self.depth, "DEPART:", args)
        item = args[0]
        name = item_name(item)
        method = getattr(self, 'depart_' + name, self.unknown)
        method(item)

    def update_attributes(self, item):
        """ Not sure if this helps or not """
        attributes = getattr(item, 'attributes', {})
        #print(attributes)
        self.attributes.update(attributes)
        #print(self.attributes)

    def log(self, item):

        return "# %s: content: %s depth: %d" % (
            item_name(item), item.astext(), self.depth)


    def unknown(self, item):

        return "# unknown: %s content: %s depth: %d" % (
            item_name(item), item.astext(), self.depth)

    def visit_section(self, item):
        """ Method or class depending on depth """
        print('SECTION')
        if not self.state:
            self.state.append(Class())
            return

        method = Method()
        self.state[0].methods.append(method)
        self.state.append(method)

    def depart_section(self, item):

        obj = self.state.pop()
        if not self.state:
            print('\n'.join(obj.dump(1)))

    def visit_title(self, item):

        obj = self.state[-1]
        obj.name = item.astext()

    def visit_paragraph(self, item):
        """ Paragraphs are docstrings """

        print('PARA:', item.astext())
        obj = self.state[-1]
        obj.doc += item.astext()


    def block_quote(self, item):
        """ Complete a function """

        result = item.astext()
        self.result = result
        
        return self._method(item, self.depth)

    def term(self, item):

        self.action = item.astext()

    def definition_list(self, item):

        pass

    def _method(self, item):

        self.parameter_string = ','.join(
            self.parameters + ['*args', '**kwargs'])
            
        template = """
        def %(name)s(self, %(parameter_string)s):

            return "%(result)s"
        """
        print("XXX Method: ", self.name)
        self.write(template)

    def _class(self, item):

        template = '''
        class %(name)s:
            """ %(doc)s """
        '''
        print("XXX Class: ", self.name)
        self.write(template, self.depth)

    def write(self, template):

        msg = template % self.__dict__

        self.response += self.form(msg)

    def form(self, msg):

        lines = msg.split('\n')
        tab = 4
        pad = " " * tab
        
        return [(self.depth * pad) + line[2*tab:]
                for line in lines]


def clean_method_name(method):

    method = method.strip(':?').replace(' ', '_')

    return method

class CodeWriter(object):

    template = ""

    def lines(self, depth):

        msg = self.template % self.__dict__

        return self.form(msg, depth)

    def form(self, msg, depth):

        lines = msg.split('\n')
        tab = 4
        pad = " " * tab
        
        return [(depth * pad) + line[tab:]
                for line in lines]


class Method(CodeWriter):

    template = '''
    def %(name)s(self, %(parameter_string)s):
        """ %(doc)s """
    
        return %(result)s
    '''

    def __init__(self):

        self.name = "method"
        self.code = "pass"
        self.doc = ""
        self.parameters = ['*args', '**kwargs']
        self.result = None

    def dump(self, depth):

        self.parameter_string = ','.join(
            self.parameters)
        
        return self.lines(depth)


class Class(CodeWriter):

    template = '''
    class %(name)s:
    """ %(doc)s """
    '''
    
    def __init__(self):

        self.name = "method"
        self.code = "pass"
        self.doc = ""

        self.methods = []

    def dump(self, depth):

        lines = self.lines(depth)

        for method in self.methods:
            lines += method.dump(depth + 1)

        return lines
            


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
