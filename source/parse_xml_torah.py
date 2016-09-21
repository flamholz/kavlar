#!/usr/bin/python
# -*- coding: utf-8 -*-
from lxml import etree
"""Parses XML intermediate format into torah model hierarchy."""

import re
import torah_model

from lxml import etree
from torah_model import FormattedText, ParashaDelimiter
from torah_model import PasukStart, PasukFragment
from torah_model import Perek, Sefer, Torah, TextFragment


# Classes that map directly to XML elements.
ONTO_XML_CLASSES = [
	Torah, Sefer, Perek, PasukStart, PasukFragment, TextFragment]

XML_CLASS_MAPPING = dict(
	(c.__name__, c)
	for c in ONTO_XML_CLASSES)
PARASHA_DELIMITER_MAPPING = dict(
	(name, ParashaDelimiter)
	for name in ParashaDelimiter.CODE_NAMES.values())
FORMATTED_TEXT_MAPPING = dict(
	(name, FormattedText)
	for name in FormattedText.CODE_NAMES.values())

XML_CLASS_MAPPING.update(PARASHA_DELIMITER_MAPPING)
XML_CLASS_MAPPING.update(FORMATTED_TEXT_MAPPING)


class XmlTorahParser(object):

	def __init__(self):
		pass

	def parse_xml_filename(self, fname):
		with open(fname, 'rU') as f:
			return self.parse_xml_file(f)

	def parse_xml_elt(self, xml_elt):
		"""Recursive parsing of an XML element."""
		tag = xml_elt.tag
		torah_model_class = XML_CLASS_MAPPING[tag]
		torah_model = torah_model_class.from_xml_elt(xml_elt)

		for child_xml_elt in xml_elt.iterchildren():
			child_torah_model = self.parse_xml_elt(child_xml_elt)
			torah_model.append_to_stream(child_torah_model)

		return torah_model

	def parse_xml_file(self, f):
		xml_root = etree.parse(f).getroot()
		torah_root = self.parse_xml_elt(xml_root)
