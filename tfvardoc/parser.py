#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from jinja2 import Environment, FileSystemLoader
import grammar

def parse(vars_file,template_file):
    with open(vars_file,'r') as f:
        vars_file = f.read()

    vars = grammar.grammar(vars_file).vars_file()
    vars = sorted(vars,key=lambda x: x['name'])

    THIS_DIR = os.getcwd()
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR),trim_blocks=True)
    out = j2_env.get_template(template_file).render(variables=vars)

    with open(template_file[:-3],'w') as f:
        f.write(out)
