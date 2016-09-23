#!/usr/bin/python
# -*- coding: utf-8 -*-

import codecs
import unittest

from lxml import etree
from os import path
from kavlar import KavlarCompiler
from parse_xml_torah import XmlTorahParser
from torah_model import Perek, TextFragment
from torah_model import Sefer, PasukStart


class XmlTorahParserTest(unittest.TestCase):

	def test_parse_shemot(self):
		fname = '../data/xml_torah/shemot.xml'
		compiler = KavlarCompiler.default_instance()

		parser = XmlTorahParser()
		root = parser.parse_xml_filename(fname)

		tex = compiler.compile_torah_model(root)
		fname = '../test_tex/test_compile.tex'
		with codecs.open(fname, 'w', encoding='utf-8') as f:
			f.write(tex)


if __name__ == '__main__':
	unittest.main()
