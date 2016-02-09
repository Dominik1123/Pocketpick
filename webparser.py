#######################################################################################
#
# This program solves the 2D puzzle "Lonpos 101".
# Copyright (C) 2016  Dominik Vilsmeier
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#######################################################################################

import re

class Parser:
	def parse(self, content):
		content = self.replace_html_special_chars(content)
		heroes=[]
		for match in re.finditer(self.regex, content):
			heroes.append(match.groupdict())
		return heroes

	def replace_html_special_chars(self, string):
		return string.replace('&#47;', '/').replace('&#39;', "'")


class AllHeroesParser(Parser):
	def __init__(self):
		self.regex=r"""<a href="(?P<url>[\-a-zA-Z/]+)"><div class="hero" style="background: url\((?P<img_url>[.\-0-9a-zA-Z/]+)\)"><div class="name">(?P<name>[a-zA-Z\s'\-]+)</div>"""


class HeroDetailParser(Parser):
	def __init__(self):
		self.regex=r"""<td><a class="link-type-hero" href="(?P<url>[\-a-zA-Z/]+)">(?P<name>[a-zA-Z\s'\-]+)</a></td><td>(?P<advantage>-?[.0-9]+)%<div class="bar bar-default"><div class="segment segment-advantage" style="width: [.0-9]+%;"></div></div></td>"""


# parser = AllHeroesParser()
# with open('example.html', 'r') as fp:
# 	heroes = parser.parse(fp.read())

# # for hero in heroes:
# # 	print hero
# print len(heroes)

# parser = HeroDetailParser()
# with open('example_hero_detail.html', 'r') as fp:
# 	heroes = parser.parse(fp.read())

# for hero in heroes:
# 	print hero
# print len(heroes)