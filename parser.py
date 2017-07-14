#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from jinja2 import Environment, FileSystemLoader
from .grammar import grammar

with open('vars.tf','r') as f:
  vars_file = f.read()

vars = grammer(vars_file).vars_file()
vars = sorted(vars,key=lambda x: x['name'])

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
j2_env = Environment(loader=FileSystemLoader(THIS_DIR),trim_blocks=True)
out = j2_env.get_template('README.md.j2').render(variables=vars)

with open('README.md','w') as f:
  f.write(out)
