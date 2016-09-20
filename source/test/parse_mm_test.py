#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

from parse_mm import MechonMamreParser


class MechonMamreParserTest(unittest.TestCase):

	def test_upper(self):
		parser = MechonMamreParser()
		sefer = parser.parse_sefer_filename('../data/mamre.cantillation/c01.htm')


if __name__ == '__main__':
	unittest.main()