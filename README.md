# Kavlar
## Introduction
Torah scrolls have many traditional formatting constraints, including fixed-width columns, forced line breaks at particular narrative points in the text and special formatting for biblical poetry, etc. Historically, expert Jewish scribes (*sof'rim*) would manually lay out a guide (called a *tikkun*, or standard) for the production of a Torah scroll. *Tikkun*s encode both normative formatting customs as well as various local traditions and some have been passed down for many generations. 

One especially challenging aspect of manually laying-out a *sefer Torah* is producing fixed-width columns by hand without excessive or insufficient whitespace between words and letters. According to tradition, some letters can be stretched in order to aid in justifying the text. These manipulations have a tendency to compromise the aesthetics and legibility of a text that is read ritually at least thrice weekly in observant Jewish communities. 

The de-facto standard for most new Torah scrolls was developed in the last 30 years by Rabbi Menachem Davidovich of Jerusalem. Davidovich's *tikkun* has 247 42-line columns, follows all *Ashkenazi* scribal traditions and uses no stretched letters. The manual production of such a layout is an incredible feat of human ingenuity, requiring an enormous degree of planning and back-tracking to achieve a fixed-width layout. Indeed, Davidovich dryly told my father Jack that it was "very hard work" ("זו הייתה עבודה קשה מעוד"). 

Over roughly the same time period, generic algorithms for automating the justification of text have progressed rapidly. The seminal publicaion in this field is due to Donald Knuth and Michael Plass, entitled "Breaking paragraphs into lines" (Software: Practice and Experience, 1981). We think of this project as mediating a virtual dialog between Knuth and Davidovich, two masters in their respective fields. 

## Overview of Kavlar Design
Kavlar is designed similarly to a two-pass compiler. The input to Kavlar is the HTML-formatted text of the Torah produced by the webmasters of [Mechon Mamre](http://mechon-mamre.org), which is parsed and converted into an intermediate XML format. The XML  can then be compiled into LateX code, where a series of macros are used to ensure that traditional formatting rules are observed. 

One difference between Kavlar and a compiler is that the intermediate XML format is designed to be manually edited. Our reasoning here is that many of the formatting constraints and traditions associated with a Torah scrolls are not included in the HTML files produced by [Mechon Mamre](http://mechon-mamre.org). As such, we produce an initial XML file by automated compilation from HTML and we subsequently edit that file to include information relevant to formatting and layout traditions. This file can then be compiled into LaTeX in a configurable fashion so that you can produce a *tikkun* observing the particular traditions of your choice. For example, two central configurations options are 
1. the number of lines per column and 
2. the aspect ratio 

## Layout Traditions
This is a partial list of the layout traditions that we know of. It is not yet clear if all of them can be respected using standard LaTeX. 

* *biya shemo* - specifies six points in the Torah that must be at the top of a column.
* *vavei ha'amudim* - a tradition where all columns begin with the letter *vav* except for the *biyah shemo* columns. 
* *nunim minuzarot* - reflected *nun*s surrounding Deuteronomy 10:35.
* special formatting for the Song of the Sea in Exodus.
* special formatting for the Song of Moses in Deuteronomy.
* special formatting for the Ten Commandments in both Exodus and Deuteronomy.

## Dependencies
Kavlar depends on the following Python libraries, which can all be installed with pip.
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) for HTML parsing
* [lxml](http://lxml.de/) for XML parsing and generation
