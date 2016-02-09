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

import httplib
import urllib
import urllib2

class WebInterface:
	def __init__(self, base_url):
		self.base_url = base_url
		self.headers = {
			'Host': 'en.dotabuff.com',
			'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Language': 'en-US,en;q=0.5',
			'Accept-Encoding': 'deflate',
			'Connection': 'keep-alive',
			'Cache-Control': 'max-age=0'
		}
		self.conn = httplib.HTTPConnection(self.base_url.split('/')[-1])

	def load_html_content(self, relative_url):
		url = self.join_urls(relative_url)
		self.conn.request('GET', url, headers=self.headers)
		response = self.conn.getresponse()
		return response.read()

	def load_image(self, relative_url):
		url = self.join_urls(relative_url)
		request = urllib2.Request(url=url, headers=self.headers)
		response = urllib2.urlopen(request)
		return response.read()
	
	def join_urls(self, relative_url):
		if relative_url[0] != '/':
			relative_url = '/' + relative_url
		return self.base_url + relative_url