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

from hero import Hero
import json
from os import path

class DataManager:
	hero_data_file_name='heroes.json'

	def load_hero_data(self):
		with open(DataManager.hero_data_file_name, 'r') as fp:
			hdata = json.load(fp)

		return [Hero(h[0], h[1], h[2]) for h in hdata]

	def save_hero_data(self, heroes):
		hdata = [(h.name, h.img_path, h.related_to) for h in heroes]
		with open(DataManager.hero_data_file_name, 'w') as fp:
			json.dump(hdata, fp)

	@staticmethod
	def save_image(img, img_path):
		with open(img_path, 'wb') as fp:
			fp.write(img)

	@staticmethod
	def convert_url_to_img_path(url, img_url):
		# return path.join('img', url.split('/')[-1]) + '.' + img_url.split('.')[-1]
		return './'+'/'.join(['img', url.split('/')[-1]]) + '.' + img_url.split('.')[-1]