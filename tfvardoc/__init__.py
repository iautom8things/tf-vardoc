#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import argparse
import parser

def tf_file(s):
    if not s.endswith('.tf'):
        raise argparse.ArgumentTypeError('must be a .tf file')
    return s

def jinja2_template(s):
    if not s.endswith('.j2'):
        raise argparse.ArgumentTypeError('must be a .j2 file')
    return s

def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-f', '--vars-file',
        type=tf_file,
        default='vars.tf',
        help='the variable file to parse (default: vars.tf)')
    arg_parser.add_argument('-t', '--template-file',
        type=jinja2_template,
        default='README.md.j2',
        help='the jinja2 template file (default: README.md.j2)')
    args = vars(arg_parser.parse_args())
    parser.parse(**args)
main()
