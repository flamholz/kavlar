#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

from lxml import etree
from os import path
from parse_xml_torah import XmlTorahParser
from torah_model import Perek, TextFragment
from torah_model import Sefer, PasukStart


class XmlTorahParserTest(unittest.TestCase):

	def _xml_to_string(self, xml_elt):
		"""Uniform tostring formatting for tests."""
		return etree.tostring(
			xml_elt, pretty_print=True, encoding='utf-8')

	def _norm_xml_string_for_fname(self, fname):
		"""Parse XML from file, write out again normalized."""
		with open(fname, 'rU') as f:
			parsed = etree.parse(f)
			return self._xml_to_string(parsed.getroot())

	def _norm_xml_string_for_torah_elt(self, torah_elt):
		"""Convert an element from torah_model into normalized XML."""
		torah_xml_elt = torah_elt.to_xml_elt()
		return self._xml_to_string(torah_xml_elt)

	def test_parse_shemot(self):
		fname = '../data/xml_torah/shemot.xml'
		expected_xml = self._norm_xml_string_for_fname(fname)

		parser = XmlTorahParser()
		shemot = parser.parse_xml_filename(fname)
		actual_xml = self._norm_xml_string_for_torah_elt(shemot)

		# XML generated from parsed tree should be equivalent to input XML.
		self.assertEquals(expected_xml, actual_xml)


if __name__ == '__main__':
	unittest.main()