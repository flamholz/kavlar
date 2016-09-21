#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

from lxml import etree
from os import path
from parse_xml_torah import XmlTorahParser
from torah_model import Perek, TextFragment
from torah_model import Sefer, PasukStart


class XmlTorahParserTest(unittest.TestCase):

	def test_parse_shemot(self):
		fname = '../data/xml_torah/shemot.xml'
		parser = XmlTorahParser()
		shemot_xml = parser.parse_xml_filename(fname)

		print shemot_xml


if __name__ == '__main__':
	unittest.main()