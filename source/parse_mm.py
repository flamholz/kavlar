#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Parses Mechon Mamre text into a torah model hierarchy.

Note that the Mechon Mamre HTML files are hand-generated. Their conventions
are not consistent between the various filetypes that you download from their
server. This code is tested with the "Hebrew with cantillation marks" files,
which were downloaded on 09/20/2016 and are checked into
	../data/mamre.cantillation/
"""

import re
import torah_model

from BeautifulSoup import BeautifulSoup


class MechonMamreParser(object):
	
	def __init__(self):
		pass

	PARASHA_PATTERN = re.compile(r'\s+({.})\s*$')

	@classmethod
	def strip_parsha_delimiter(cls, text):
		spaceless = text.strip()
		ms = re.findall(cls.PARASHA_PATTERN, spaceless)
		if not ms:
			return spaceless, None

		delim = ms[0].strip('{}')
		stripped = re.sub(cls.PARASHA_PATTERN, '', spaceless)
		return stripped, delim

	@staticmethod
	def get_tag_name(node):
		"""Given a generic BeautifulSoup node, returns the tag name."""
		if hasattr(node, 'name'):
			return node.name.lower()
		return None

	# Tags on which to break the fragment
	BREAKING_TAGS = ('br', 'b')

	def parse_sefer_filename(self, fname, sefer_idx=0):
		"""Parses the Mechon Mamre file pointed to by f.

		Args:
			fname: path to Mechon Mamre file.
		"""
		with open(fname, 'rU') as f:
			return self.parse_sefer_file(f, sefer_idx)

	def parse_sefer_file(self, f, sefer_idx=0):
		"""Parses the Mechon Mamre sefer file pointed to by f.

		Args:
			f: file handle to Mechon Mamre file.
		"""

		parsed = BeautifulSoup(f)
		seforim = parsed.findChildren(name='h1')
		sefer_id = 'sefer_%d' % sefer_idx
		sefer = torah_model.Sefer(seforim[0].text, sefer_idx, sefer_id)

		perek_idx = -1
		pasuk_idx = -1
		current_perek = None
		perek_pasuk_children = parsed.findChildren(name='b')

		for i, pp in enumerate(perek_pasuk_children):
			perek_str, pasuk_str = pp.text.split(',')

			# May need to open a new perek.
			if (current_perek is None or
				current_perek.perek != perek_str):
				perek_idx += 1
				pasuk_idx = -1  # Reset pasuk counter
				perek_id = 'perek_%d:%d' % (sefer_idx, perek_idx)
				current_perek = torah_model.Perek(
					perek_str, perek_idx, perek_id)
				sefer.append_to_stream(current_perek)

			# Mark the start of a new pasuk.
			pasuk_idx += 1
			pasuk_id = 'pasuk_%d:%d:%d' % (sefer_idx, perek_idx, pasuk_idx)
			# TODO: how do we handle the case the petuha/setumah
			# come in the middle of a pasuk?
			current_pasuk = torah_model.PasukStart(
				pasuk_str, pasuk_idx, pasuk_id)
			current_perek.append_to_stream(current_pasuk)

			# Iterate over the text of the pasuk, until we hit the next one.
			sib = pp.nextSibling
			accumulated_pasuk = []
			while sib:
				tag_name = self.get_tag_name(sib)
				if tag_name and tag_name.lower() in self.BREAKING_TAGS:
					break

				accumulated_pasuk.append(unicode(sib))
				sib = sib.nextSibling

			pasuk_text = ''.join(accumulated_pasuk)
			pasuk_text, delim = self.strip_parsha_delimiter(pasuk_text)
			text_frag = torah_model.TextFragment(pasuk_text)
			current_perek.append_to_stream(text_frag)

			if delim is not None:
				pdelim = torah_model.ParashaDelimiter.from_letter_code(delim)
				current_perek.append_to_stream(pdelim)

		return sefer

	def parse_torah_files(self, fs):
		"""Parses a list of Sefer files into a Torah object."""
		t = torah_model.Torah()
		for i, f in enumerate(fs):
			sefer = self.parse_sefer_file(f, sefer_idx=i)
			t.append_to_stream(sefer)
		return t

	def parse_torah_filenames(self, fnames):
		"""Parses a list of Sefer files into a Torah object."""
		t = torah_model.Torah()
		for i, fname in enumerate(fnames):
			sefer = self.parse_sefer_filename(fname, sefer_idx=i)
			t.append_to_stream(sefer)
		return t


