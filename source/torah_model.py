#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Classes describing the object model of a sefer torah or tikkun."""


class Stream(object):
	def append_to_stream(self, elt):
		self.stream.append(elt)


class Sefer(Stream):
	"""Which of the books, e.g. Genesis, Exodus etc."""
	def __init__(self, name):
		self.name = name
		self.stream = []

	def __unicode__(self):
		return self.name

	def __str__(self):
		return unicode(self.name).encode('utf-8')

	def append_to_stream(self, elt):
		self.stream.append(elt)


class Perek(Stream):
	"""A chapter marker. Contains text fragments and various markers."""
	def __init__(self, perek):
		"""Initialize.

		Args:
			perek: the Hebrew perek demarcation.
		"""
		self.perek = perek
		self.stream = []

	def __unicode__(self):
		return self.perek

	def __str__(self):
		return unicode(self.perek).encode('utf-8')


class PasukStart(object):
	"""Demarcates the start of a new verse."""
	def __init__(self, pasuk):
		"""Initialize.

		Args:
			perek: the Hebrew perek demarcation.
		"""
		self.pasuk = pasuk

	def __unicode__(self):
		return self.perek

	def __str__(self):
		return unicode(self.perek).encode('utf-8')


class TextFragment(object):
	"""A fragment of text contained within a sefer."""

	def __init__(self, text):
		"""A fragment of a verse.

		Usually contains the whole verse, except in weird scenarios
		where the verse is split by a ParashaDelimiter. Markup may
		be included in the verse text in the event of special
		formatting for a character, for example the big/small letters.
		

		Args:
			text: the Hebrew text of the the verse fragment.
				May include markup.
		"""
		self.text = text

	def __unicode__(self):
		return self.text

	def __str__(self):
		return unicode(self.text).encode('utf-8')


class ParashaDelimiter(object):
	PETUHA = -1
	SETUMA = -2
	BOOK_END = -3
	SHIRAH_LINE_BREAK = -4
	CODE_MAP = {
		u"פ": PETUHA,
		u"ס": SETUMA,
		u"ש": BOOK_END,
		u"ר": SHIRAH_LINE_BREAK
	}
	CODE_NAMES = {
		PETUHA: "PETUHA",
		SETUMA: "SETUMA",
		BOOK_END: "END OF BOOK",
		SHIRAH_LINE_BREAK: "SHIRAT HAYAM LINE BREAK"
	}

	def __init__(self, kind=None):
		self.kind = kind

	@classmethod
	def from_letter_code(cls, letter_code):
		kind = cls.CODE_MAP[letter_code]
		return ParashaDelimiter(kind)

	def __str__(self):
		return '<%s />' % self.CODE_NAMES[self.kind]
