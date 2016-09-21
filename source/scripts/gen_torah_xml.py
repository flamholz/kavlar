#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Configurable script for generating XML from the Mechon Mamre HTML format."""


import argparse
import json

from lxml import etree
from os import path
from parse_mm import MechonMamreParser
from torah_model import Perek, TextFragment, Sefer


def main():
	parser = argparse.ArgumentParser(
		description='Converts Mechon Mamre HTML to XML.')
	parser.add_argument(
		'-c', '--config_filename', dest='config_filename',
		default='scripts/gen_torah_xml_config.json',
		help='Paths of JSON config file.')
	args = parser.parse_args()

	# Load JSON configuration file.
	print 'Reading configuration from', args.config_filename
	assert path.exists(args.config_filename)
	with open(args.config_filename, 'rU') as config_f:
		config = json.load(config_f)

	html_filenames = config['html_filenames']
	output_filename = config['output_filename']

	print 'Parsing files:'
	for fname in html_filenames:
		print fname

	parser = MechonMamreParser()
	torah = parser.parse_torah_filenames(html_filenames)
	torah_xml_elt = torah.to_xml_elt()

	print 'Writing XML output to', output_filename
	with open(output_filename, 'w') as out_f:
		xml_data = etree.tostring(
			torah_xml_elt, pretty_print=True, encoding='utf-8')
		out_f.write(xml_data)


if __name__ == '__main__':
	main()