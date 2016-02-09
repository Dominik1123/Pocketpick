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

from PyQt4 import QtGui, QtCore
from time import sleep
from datamanager import DataManager
from hero import Hero
from webinterface import WebInterface
from webparser import AllHeroesParser, HeroDetailParser

class DownloadManager(QtCore.QObject):
	hero_loaded = QtCore.pyqtSignal('QString', 'int', 'int')
	job_done = QtCore.pyqtSignal()

	base_url='http://www.dotabuff.com'
	all_heroes_url='/heroes'

	def __init__(self, parent=None):
		super(DownloadManager, self).__init__(parent)

	def start(self, pause_sec=2):
		wi = WebInterface(DownloadManager.base_url)
		wp_all = AllHeroesParser()
		wp_detail = HeroDetailParser()

		heroes_all = wp_all.parse(wi.load_html_content(DownloadManager.all_heroes_url))

		self.heroes = []
		for i, hero in enumerate(heroes_all):
			img_path = DataManager.convert_url_to_img_path(hero['url'], hero['img_url'])

			sleep(pause_sec)
			details = wp_detail.parse(wi.load_html_content(hero['url']))

			related_to = {}
			for related_hero in details:
				related_to[related_hero['name']] = related_hero['advantage']

			self.heroes.append(Hero(name=hero['name'], img_path=img_path, related_to=related_to))

			try:
				with open(img_path, 'rb') as fp:
					pass
			except IOError:  # image file not found
				sleep(pause_sec)
				DataManager.save_image(wi.load_image(hero['img_url']), img_path)

			self.hero_loaded.emit(hero['name'], i+1, len(heroes_all))

		self.job_done.emit()