#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Compiles a torah model hierarchy into LaTeX code with various options.

"""

import re
import tex_templating
import torah_model

from ConfigParser import SafeConfigParser


class KavlarConfig(object):

	@classmethod
	def default_config(cls):
		"""TODO: add templating configuration for LaTeX."""
		config = SafeConfigParser()
		config.add_section('formatting')
		config.set('formatting', 'aspect_ratio', '4.0')
		config.set('formatting', 'lines_per_col', '42')
		config.set('formatting', 'font', 'Stam Ashkenaz CLM')
		config.set('formatting', 'strip_vowels', 'True')
		config.set(
			'formatting', 'strip_cantillation_marks', 'True')
		config.add_section('templates')
		config.set(
			'templates', 'template_path', 'templates')
		return config

	@classmethod
	def read_config(cls, fname):
		return cls.default_config().read(fname)


class KavlarCompiler(object):

	def __init__(self, config):
		self.config = config

		t_path = config.get('templates', 'template_path')
		self.template_env = tex_templating.make_tex_env(
			t_path)

	@classmethod
	def default_instance(cls):
		return cls(KavlarConfig.default_config())

	def config_template_data(self):
		"""Generates an initial dict with data from the config."""
		template_data = {
			'config': {
				'font': self.config.get('formatting', 'font'),
				'aspect_ratio': self.config.get('formatting', 'aspect_ratio'),
				'lines_per_col': self.config.get('formatting', 'lines_per_col')
			}
		}
		return template_data

	def compile_torah_model(self, root_torah_elt):
		assert type(root_torah_elt) == torah_model.Torah

		template_data = self.config_template_data()
		template_data.update({
			'tikkun_content': root_torah_elt.to_tex(self.config)
			})

		# Render from template that includes header/footer
		template = self.template_env.get_template('tikkun.tex')
		return template.render(template_data)
