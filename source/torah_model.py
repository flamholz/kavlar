#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Classes describing the object model of a sefer torah or tikkun."""

from lxml import etree


class XmlAble(object):
	def add_to_xml_tree(self, xml_elt):
		"""Append thyself to this container element as appropriate."""
		msg = (
			'%s does not implement add_to_xml_tree' %
			self.__class__.__name__)
		raise NotImplementedError(msg)


class Stream(XmlAble):
	def append_to_stream(self, elt):
		self.stream.append(elt)

	@property
	def iter_stream(self):
		return iter(self.stream)

	def add_stream_to_xml_tree(self, xml_elt):
		"""Elements in the stream must implement XmlAble."""
		for child in self.iter_stream:
			child.add_to_xml_tree(xml_elt)


class Torah(Stream):
	"""Ordered stream of Sefarim."""
	def __init__(self):
		self.stream = []

	def to_xml_elt(self):
		self_xml = etree.Element(
			self.__class__.__name__)
		self.add_stream_to_xml_tree(self_xml)
		return self_xml

	def add_to_xml_tree(self, xml_elt):
		self_xml = self.to_xml_elt()
		xml_elt.append(self_xml)


class Sefer(Stream):
	"""Which of the books, e.g. Genesis, Exodus etc."""
	def __init__(self, name, sefer_idx, sefer_id):
		"""Initialize.

		Args:
			name: the name of the Sefer (Hebrew).
			sefer_idx: the index of the Sefer in the compilation.
			sefer_id: a unique identifier for this sefer.
		"""
		self.name = name
		self.sefer_idx = sefer_idx
		self.sefer_id = sefer_id
		self.stream = []

	def __unicode__(self):
		return self.name

	def __str__(self):
		return unicode(self.name).encode('utf-8')

	def append_to_stream(self, elt):
		self.stream.append(elt)

	def add_to_xml_tree(self, xml_elt):
		self_xml = etree.Element(
			self.__class__.__name__, name=self.name,
			id=self.sefer_id, index=str(self.sefer_idx))
		self.add_stream_to_xml_tree(self_xml)
		xml_elt.append(self_xml)


class Perek(Stream):
	"""A chapter marker. Contains text fragments and various markers."""
	def __init__(self, perek, perek_idx, perek_id):
		"""Initialize.

		Args:
			perek: the Hebrew perek demarcation.
			perek_idx: the index of the perek in the sefer.
			perek_id: a unique identifier for this perek.
		"""
		self.perek = perek
		self.perek_idx = perek_idx
		self.perek_id = perek_id
		self.stream = []

	def __unicode__(self):
		return self.perek

	def __str__(self):
		return unicode(self.perek).encode('utf-8')

	def add_to_xml_tree(self, xml_elt):
		self_xml = etree.Element(
			self.__class__.__name__, perek=self.perek,
			id=self.perek_id, index=str(self.perek_idx))
		self.add_stream_to_xml_tree(self_xml)
		xml_elt.append(self_xml)


class PasukStart(XmlAble):
	"""Demarcates the start of a new verse."""
	def __init__(self, pasuk, pasuk_idx, pasuk_id):
		"""Initialize.

		Args:
			pasuk: the Hebrew pasuk demarcation.
			pasuk_idx: the index of the pasuk in the perek.
			pasuk_id: a unique identifier for this pasuk.
		"""
		self.pasuk = pasuk
		self.pasuk_idx = pasuk_idx
		self.pasuk_id = pasuk_id

	def __unicode__(self):
		return self.perek

	def __str__(self):
		return unicode(self.perek).encode('utf-8')

	def add_to_xml_tree(self, xml_elt):
		self_xml = etree.Element(
			self.__class__.__name__, pasuk=self.pasuk,
			id=self.pasuk_id, index=str(self.pasuk_idx))
		xml_elt.append(self_xml)


class TextFragment(XmlAble):
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

	def add_to_xml_tree(self, xml_elt):
		# Hack to avoid escaping of the markup in self.text.
		xml_text = '<TextFragment>%s</TextFragment>' % self.text
		self_xml = etree.XML(xml_text)
		xml_elt.append(self_xml)


class ParashaDelimiter(XmlAble):
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
		PETUHA: "Petuha",
		SETUMA: "Setumah",
		BOOK_END: "SeferEnd",
		SHIRAH_LINE_BREAK: "ShiratHayamLineBreak"
	}

	def __init__(self, kind=None):
		self.kind = kind

	@classmethod
	def from_letter_code(cls, letter_code):
		kind = cls.CODE_MAP[letter_code]
		return ParashaDelimiter(kind)

	def __str__(self):
		return '<%s />' % self.CODE_NAMES[self.kind]

	@property
	def xml_name(self):
		return self.CODE_NAMES[self.kind]

	def add_to_xml_tree(self, xml_elt):
		self_xml = etree.Element(self.xml_name)
		xml_elt.append(self_xml)
