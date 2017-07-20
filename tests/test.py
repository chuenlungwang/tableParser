# -*- coding: utf-8 -*-

import os

from .context import parser

if __name__ == '__main__' :
    xml_file = './tests/parser.xml'
    directory = os.path.dirname(xml_file)
    parser.parse(xml_file, directory, "build")
