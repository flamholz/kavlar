#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Compiles a torah model hierarchy into LaTeX code with various options.

"""

import re
import torah_model

from ConfigParser import SafeConfigParser


class KavlarConfig(object):

	@classmethod
	def default_config(cls):
		config = SafeConfigParser()
		config.add_section('formatting')
		config.set('formatting', 'aspect_ratio', '4.0')
		config.set('formatting', 'lines_per_col', '42')
		config.set('formatting', 'font', 'Stam Ashkenaz CLM')
		config.set('formatting', 'strip_vowels', 'True')
		config.set(
			'formatting', 'strip_cantillation_marks', 'True')
		return config

	@classmethod
	def read_config(cls, fname):
		return cls.default_config().read(fname)


class KavlarCompiler(object):

	def __init__(self, config):
		self.config = config

	@classmethod
	def default_instance(cls):
		return cls(KavlarConfig.default_config())

	@property
	def aspect_ratio(self):
		return self.config.get('aspect_ratio')

	@property
	def lines_per_col(self):
		return self.config.get('lines_per_col')

	def compile_torah_model(self, root_torah_elt):
		assert type(root_torah_elt) == torah_model.Torah
		return root_torah_elt.to_tex(self.config)
	