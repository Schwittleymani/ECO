# -*- coding: utf-8 -*-
from __future__ import print_function

from IPython import (
    display, 
    get_ipython
)
from IPython.core.magic import (
    Magics, 
    magics_class, 
    line_cell_magic
)
import jinja2
# A new piece of the jinja API
# Gives access to the abstract syntax tree
from jinja2 import meta
import yaml
import requests

@magics_class
class JinjaMagics(Magics):
    '''Magics class containing the jinja2 magic and state'''
    
    def __init__(self, shell):
        super(JinjaMagics, self).__init__(shell)
    
    @line_cell_magic
    def jinja(self, methods, cell=''):
        '''
        methods :: line
        cell :: cell
        
        jinja2 cell magic function.  Contents of cell are rendered by jinja2, and 
        the line can be used to specify output type.
        '''
        
        def mapNstoContext( template ):
            '''
            Map the namespace variables to Jinja template context
            '''
            context = {}
            for ns in listVar(template):
                context[ns] = ip.user_ns[ns]
            return context

        def listVar( template ):
            '''
            return list the variables in template
            '''
            source = self.env.loader.get_source(self.env,template)
            # Jinja Abstract Syntax Tree
            ast = self.env.parse(
                source
            )
            return list(
                meta.find_undeclared_variables(ast)
            )
        
        methods = methods.strip().split()
        
        if len(methods) > 0 and methods[0] == 'loader':
            # Initialize the Jinja magic Environment with the DictLoader
            if len(methods) > 1 and methods[1] == 'append':
                # Add a new template from the cell string
                # %%jinja loader append name-of-template.html
                if len(methods)>3 and methods[3] == 'from':
                    cell = requests.get( methods[4] ).text
                self.env.loader.mapping[methods[2]] = cell
                self.env.loader = jinja2.DictLoader(self.env.loader.mapping)
                return self.env.loader.mapping
            elif len(methods) > 1 and methods[1] == 'yaml':
                #Load template from a yaml context
                # %%jinja loader yaml
                # template1: >
                #    <div>{{variable}}</div>
                ### add functionality to get from information urls and the file system ###
                self.env = jinja2.Environment(
                    loader = jinja2.DictLoader( yaml.safe_load(cell) )
                )
                return self.env.loader.mapping
            else:
                #Execute python to get template
                # %%jinja 
                # {
                #  'template1': ' <div>{{variable}}</div>'
                # }
                self.env = jinja2.Environment(
                    loader = jinja2.DictLoader( ip.ev( cell ) )
                )
            return self.env.loader.mapping 
        else:
            # execute the code cell before creawting the template
            ip.run_code(cell)
            # Render a template using the existing variable names
            out = []
            for method in methods:
                out.append(self.env.get_template(method).render( mapNstoContext( method ) ))
            return display.HTML( '\n'.join(out) )
        
ip = get_ipython()
ip.register_magics(JinjaMagics)