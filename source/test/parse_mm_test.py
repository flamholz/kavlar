#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

from parse_mm import MechonMamreParser
from torah_model import Perek, TextFragment


class MechonMamreParserTest(unittest.TestCase):

	def test_parse_sefer_filename(self):
		parser = MechonMamreParser()
		sefer = parser.parse_sefer_filename('../data/mamre.cantillation/c01.htm')

		for perek in sefer.iter_stream:
			self.assertEquals(Perek, type(perek))

		n_perakim = len(sefer.stream)
		expected_perakim = 50  # Bereshit has 50
		self.assertEquals(expected_perakim, n_perakim)

		# For a particular perek, check it has the right
		# number of psukim - same as number of TextFragments
		# except in very strange cases where psukim are broken
		# with a petuha/setumah which does not happen in Bereshit.
		random_perek = 13     # index 13 is perek 14
		expected_psukim = 24  # has 24 psukim
		actual_psukim = 0
		perek = sefer.stream[random_perek]
		for elt in perek.iter_stream:
			if type(elt) == TextFragment:
				actual_psukim += 1
		self.assertEquals(expected_psukim, actual_psukim)
		

if __name__ == '__main__':
	unittest.main()