#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

from parse_mm import MechonMamreParser
from torah_model import Perek


class MechonMamreParserTest(unittest.TestCase):

	def test_parse_sefer_filename(self):
		parser = MechonMamreParser()
		sefer = parser.parse_sefer_filename('../data/mamre.cantillation/c01.htm')

		for perek in sefer.iter_stream:
			self.assertEquals(Perek, type(perek))


if __name__ == '__main__':
	unittest.main()